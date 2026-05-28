"""
Secure File Sharing Routes
API endpoints for encrypted file sharing with JWT and OTP authentication
"""

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

from auth.jwt_handler import JWTHandler


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
    share_id: str,
    email: str = Depends(get_email_from_token),
    token: str = Depends(get_authorization_token)
):
    """
    Get detailed information about a file share
    User must be sender or recipient
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

        if (
            email != file_share.sender_email
            and email != file_share.recipient_email
        ):
            raise HTTPException(
                status_code=401,
                detail="Not authorized"
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
