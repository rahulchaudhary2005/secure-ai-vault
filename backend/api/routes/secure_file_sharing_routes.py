"""
Secure File Sharing Routes
API endpoints for encrypted file sharing with JWT and OTP authentication
"""
import os
import base64

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Header,
    HTTPException,
    Depends
)

from typing import Optional

from api.controllers.secure_file_sharing_controller import (
    SecureFileSharingController,
    InitEncryptionRequest,
    VerifyEncryptionOTPRequest,
    UploadForEncryptionRequest,
    RequestDecryptionAccessRequest,
    VerifyDecryptionOTPRequest,
    DecryptFileRequest
)
from pydantic import BaseModel
from auth.jwt_handler import JWTHandler

from fastapi.responses import StreamingResponse
from io import BytesIO


# =========================
# ROUTER INITIALIZATION
# =========================

router = APIRouter(
    prefix="/api/secure-share",
    tags=["Secure File Sharing"]
)


# =========================
# DEPENDENCY INJECTIONS
# =========================

async def get_authorization_token(
    authorization: Optional[str] = Header(None)
) -> str:
    """Extract and validate authorization token"""

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header"
        )

    try:
        scheme, token = authorization.split()
        
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization scheme"
            )

        return token

    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format"
        )


def get_email_from_token(
    token: str = Depends(get_authorization_token)
) -> str:
    """Extract email from JWT token"""

    email = JWTHandler.extract_email_from_token(token)

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return email


# =========================
# ENCRYPTION PHASE ROUTES
# =========================

@router.post("/encrypt/init")
async def init_encryption(
    request: InitEncryptionRequest
):
    """
    Step 1: Initialize secure file sharing
    Initiates OTP verification for both sender and recipient
    
    Required: sender_email, recipient_email
    Returns: session IDs for both parties
    """

    return await (
        SecureFileSharingController.init_encryption(request)
    )


@router.post("/encrypt/verify-otp")
async def verify_encryption_otp(
    request: VerifyEncryptionOTPRequest,
    user_email: str = Header(...),
    user_role: str = Header(...)
):
    """
    Step 2: Verify OTP for encryption initiation
    Both sender and recipient must verify their OTP
    
    Headers: user_email, user_role (sender/recipient)
    Returns: JWT access token for file upload
    """

    return await (
        SecureFileSharingController
        .verify_encryption_otp(
            request,
            user_email,
            user_role
        )
    )


@router.post("/encrypt/upload")
async def upload_and_encrypt_file(
    file: UploadFile = File(...),
    sender_email: str = Header(...),
    recipient_email: str = Header(...),
    password: str = Header(...),
    authorization: str = Header(...),
    token: str = Depends(get_authorization_token)
):
    """
    Step 3: Upload file and encrypt with metadata preservation
    Only sender can perform this operation
    
    Headers: 
        - sender_email
        - recipient_email
        - password (for encryption)
        - authorization (Bearer JWT token)
    
    File: Binary file to encrypt
    
    Returns: share_id and file info
    """

    return await (
        SecureFileSharingController
        .upload_and_encrypt_file(
            file,
            sender_email,
            recipient_email,
            password,
            token
        )
    )


# =========================
# DECRYPTION PHASE ROUTES
# =========================

@router.post("/decrypt/request")
async def request_decryption_access(
    request: RequestDecryptionAccessRequest
):
    """
    Step 1: Request decryption access
    Recipient initiates decryption request
    
    Required: share_id, recipient_email
    Returns: session_id and OTP delivery confirmation
    """

    return await (
        SecureFileSharingController
        .request_decryption_access(request)
    )


@router.post("/decrypt/verify-otp")
async def verify_decryption_otp(
    request: VerifyDecryptionOTPRequest,
    recipient_email: str = Header(...)
):
    """
    Step 2: Verify OTP for decryption
    Recipient must verify OTP received on their email
    
    Headers: recipient_email
    Returns: JWT access token for file decryption
    """

    return await (
        SecureFileSharingController
        .verify_decryption_otp(
            request,
            recipient_email
        )
    )


@router.post("/decrypt/download")
async def decrypt_and_download_file(
    request: DecryptFileRequest,
    recipient_email: str = Header(...),
    authorization: str = Header(...),
    token: str = Depends(get_authorization_token)
):
    """
    Step 3: Decrypt file and prepare for download
    Only verified recipient can decrypt
    
    Headers:
        - recipient_email
        - authorization (Bearer JWT token)
    
    Body: share_id, password
    
    Returns: Decrypted file data with metadata
    """

    return await (
        SecureFileSharingController
        .decrypt_and_download_file(
            request.share_id,
            request.password,
            recipient_email,
            token
        )
    )


# =========================
# STATUS & INFORMATION ROUTES
# =========================

@router.get("/shares/sent")
async def get_sent_shares(
    email: str = Depends(get_email_from_token),
    token: str = Depends(get_authorization_token)
):
    """
    Get all files shared by current user
    Requires: Valid JWT token
    """

    try:
        from database.file_share_repository import (
            FileShareRepository
        )

        shares = (
            FileShareRepository.get_user_shares(
                email,
                role="sender"
            )
        )

        return {
            "success": True,
            "email": email,
            "shares": [
                {
                    "share_id": share.share_id,
                    "recipient_email": (
                        share.recipient_email
                    ),
                    "filename": (
                        share.original_filename
                    ),
                    "status": share.status,
                    "created_at": (
                        share.created_at.isoformat()
                    ),
                    "accessed_at": (
                        share.accessed_at.isoformat()
                        if share.accessed_at
                        else None
                    )
                }
                for share in shares
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve shares: {str(e)}"
        )


@router.get("/shares/received")
async def get_received_shares(
    email: str = Depends(get_email_from_token),
    token: str = Depends(get_authorization_token)
):
    """
    Get all files shared with current user
    Requires: Valid JWT token
    """

    try:
        from database.file_share_repository import (
            FileShareRepository
        )

        shares = (
            FileShareRepository.get_user_shares(
                email,
                role="recipient"
            )
        )

        return {
            "success": True,
            "email": email,
            "shares": [
                {
                    "share_id": share.share_id,
                    "sender_email": share.sender_email,
                    "filename": (
                        share.original_filename
                    ),
                    "size": share.file_size,
                    "mime_type": share.mime_type,
                    "status": share.status,
                    "created_at": (
                        share.created_at.isoformat()
                    ),
                    "expires_at": (
                        share.expires_at.isoformat()
                        if share.expires_at
                        else None
                    )
                }
                for share in shares
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve shares: {str(e)}"
        )


@router.get("/share/{share_id}/info")
async def get_share_info(
    share_id: str
):
    """
    Get detailed information about a file share
    Share lookup is allowed by secret share ID only.
    """

    try:
        from database.file_share_repository import (
            FileShareRepository
        )

        file_share = (
            FileShareRepository.get_by_share_id(share_id)
        )

        if not file_share:
            raise HTTPException(
                status_code=404,
                detail="Share not found"
            )

        return {
            "success": True,
            "share": {
                "share_id": file_share.share_id,
                "sender_email": file_share.sender_email,
                "recipient_email": (
                    file_share.recipient_email
                ),
                "filename": (
                    file_share.original_filename
                ),
                "size": file_share.file_size,
                "mime_type": file_share.mime_type,
                "status": file_share.status,
                "sender_verified": (
                    file_share.sender_otp_verified
                ),
                "recipient_verified": (
                    file_share.recipient_otp_verified
                ),
                "created_at": (
                    file_share.created_at.isoformat()
                ),
                "expires_at": (
                    file_share.expires_at.isoformat()
                    if file_share.expires_at
                    else None
                ),
                "accessed_at": (
                    file_share.accessed_at.isoformat()
                    if file_share.accessed_at
                    else None
                )
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve share info: {str(e)}"
        )
# =========================
# DOWNLOAD ORIGINAL FILE
# =========================

@router.get("/download/original/{share_id}")
async def download_original_file(
    share_id: str,
    email: str = Depends(get_email_from_token)
):

    try:

        from database.file_share_repository import (
            FileShareRepository
        )

        file_share = (
            FileShareRepository.get_by_share_id(
                share_id
            )
        )

        if not file_share:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        # =========================
        # VERIFY OWNER
        # =========================

        if file_share.sender_email != email:

            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )

        file_path = (
            file_share.encrypted_file_path
        )

        if not os.path.exists(file_path):

            raise HTTPException(
                status_code=404,
                detail="Encrypted file missing"
            )

        file_data = open(
            file_path,
            "rb"
        ).read()

        return StreamingResponse(

            BytesIO(file_data),

            media_type="application/octet-stream",

            headers={
                "Content-Disposition":
                f'attachment; filename="encrypted_{file_share.original_filename}"'
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# DOWNLOAD DECRYPTED FILE
# =========================

@router.post("/download/decrypted/{share_id}")
async def download_decrypted_file(

    share_id: str,

    request: DecryptFileRequest,

    recipient_email: str = Header(...),

    token: str = Depends(get_authorization_token)
):

    try:

        result = await (
            SecureFileSharingController
            .decrypt_and_download_file(

                share_id=share_id,

                password=request.password,

                recipient_email=recipient_email,

                access_token=token
            )
        )

        if not result["success"]:

            raise HTTPException(
                status_code=400,
                detail="Decryption failed"
            )

        file_bytes = base64.b64decode(
            result["file_data"]
        )

        metadata = result["metadata"]

        return StreamingResponse(

            BytesIO(file_bytes),

            media_type=metadata["mime_type"],

            headers={
                "Content-Disposition":
                f'attachment; filename="{metadata["filename"]}"'
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )