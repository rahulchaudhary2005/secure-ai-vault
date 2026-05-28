"""
Secure File Sharing Controller
Manages encryption, OTP verification, and decryption with JWT authentication
"""

import os
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, UploadFile
from pydantic import BaseModel

from database.file_share_repository import FileShareRepository
from database.otp_session_repository import OTPSessionRepository
from database.user_repository import UserRepository

from encryption.enhanced_file_encryption import EnhancedFileEncryption
from auth.jwt_handler import JWTHandler
from auth.email_sender import EmailSender
from auth.otp_manager import OTPManager
from auth.email_validator import EmailValidator

from storage.storage_manager import StorageManager
from utils.constants import UPLOAD_DIR
from utils.helpers import generate_secure_filename


# =========================
# REQUEST/RESPONSE MODELS
# =========================

class InitEncryptionRequest(BaseModel):
    sender_email: str
    recipient_email: str
    file_description: Optional[str] = None


class VerifyEncryptionOTPRequest(BaseModel):
    session_id: str
    otp_code: str


class UploadForEncryptionRequest(BaseModel):
    session_id: str
    password: str


class RequestDecryptionAccessRequest(BaseModel):
    share_id: str
    recipient_email: str


class VerifyDecryptionOTPRequest(BaseModel):
    session_id: str
    otp_code: str


class DecryptFileRequest(BaseModel):
    share_id: str
    password: str


# =========================
# SECURE FILE SHARING CONTROLLER
# =========================

class SecureFileSharingController:
    """
    Enterprise-grade secure file sharing
    with dual-email OTP verification and JWT authentication
    """

    # =========================
    # ENCRYPTION PHASE
    # =========================

    @staticmethod
    async def init_encryption(
        request: InitEncryptionRequest
    ) -> dict:
        """
        Step 1: Initialize secure file sharing
        - Validate emails
        - Generate OTP for sender and recipient
        - Create session
        """

        try:
            # =========================
            # VALIDATE EMAILS
            # =========================

            sender_email = EmailValidator.validate(
                request.sender_email
            )

            recipient_email = EmailValidator.validate(
                request.recipient_email
            )

            if not sender_email or not recipient_email:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid email addresses"
                )

            if sender_email == recipient_email:
                raise HTTPException(
                    status_code=400,
                    detail="Sender and recipient must be different"
                )

            # =========================
            # VERIFY USERS EXIST
            # =========================

            sender = UserRepository.get_by_email(sender_email)
            recipient = UserRepository.get_by_email(recipient_email)

            if not sender or not recipient:
                raise HTTPException(
                    status_code=401,
                    detail="One or both users not found"
                )

            # =========================
            # GENERATE OTP FOR SENDER
            # =========================

            sender_otp = OTPManager.generate_otp()

            sender_session = (
                OTPSessionRepository
                .create_otp_session(
                    email=sender_email,
                    otp_code=sender_otp,
                    operation_type="sender",
                    expires_in_minutes=10
                )
            )

            # =========================
            # GENERATE OTP FOR RECIPIENT
            # =========================

            recipient_otp = OTPManager.generate_otp()

            recipient_session = (
                OTPSessionRepository
                .create_otp_session(
                    email=recipient_email,
                    otp_code=recipient_otp,
                    operation_type="recipient",
                    expires_in_minutes=10
                )
            )

            # =========================
            # SEND OTP EMAILS
            # =========================

            await EmailSender.send_otp_email(
                sender_email,
                sender_otp
            )

            await EmailSender.send_otp_email(
                recipient_email,
                recipient_otp
            )

            return {
                "success": True,
                "message": (
                    "OTP codes sent to both emails. "
                    "Sender and recipient must verify."
                ),
                "sender_session_id": sender_session.session_id,
                "recipient_session_id": (
                    recipient_session.session_id
                ),
                "sender_email": sender_email,
                "recipient_email": recipient_email,
                "expires_in_minutes": 10
            }

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Encryption init failed: {str(e)}"
            )

    @staticmethod
    async def verify_encryption_otp(
        request: VerifyEncryptionOTPRequest,
        user_email: str,
        user_role: str
    ) -> dict:
        """
        Step 2: Verify OTP for encryption
        user_role: "sender" or "recipient"
        """

        try:
            # =========================
            # VERIFY OTP
            # =========================

            result = OTPSessionRepository.verify_otp(
                request.session_id,
                request.otp_code
            )

            if not result["success"]:
                raise HTTPException(
                    status_code=400,
                    detail=result["message"]
                )

            otp_session = result["otp_session"]

            # =========================
            # VERIFY EMAIL MATCHES
            # =========================

            if otp_session.email != user_email:
                raise HTTPException(
                    status_code=401,
                    detail="Email mismatch"
                )

            # =========================
            # VERIFY OPERATION TYPE
            # =========================

            if otp_session.operation_type != user_role:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid role: expected {user_role}"
                    )
                )

            # =========================
            # CREATE JWT ACCESS TOKEN
            # =========================

            access_token = JWTHandler.create_access_token(
                {
                    "sub": user_email,
                    "email": user_email,
                    "role": user_role,
                    "verified_at": (
                        datetime.utcnow().isoformat()
                    )
                }
            )

            return {
                "success": True,
                "message": (
                    f"{user_role.capitalize()} OTP verified"
                ),
                "access_token": access_token,
                "token_type": "bearer",
                "session_id": request.session_id
            }

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"OTP verification failed: {str(e)}"
            )

    @staticmethod
    async def upload_and_encrypt_file(
        file: UploadFile,
        sender_email: str,
        recipient_email: str,
        password: str,
        access_token: str
    ) -> dict:
        """
        Step 3: Upload file and encrypt with metadata preservation
        """

        try:
            # =========================
            # VALIDATE JWT TOKEN
            # =========================

            token_result = JWTHandler.verify_token(
                access_token
            )

            if not token_result["success"]:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
                )

            payload = token_result["payload"]

            if (
                payload.get("email") != sender_email
                or payload.get("role") != "sender"
            ):
                raise HTTPException(
                    status_code=401,
                    detail="Unauthorized"
                )

            # =========================
            # READ FILE
            # =========================

            file_content = await file.read()

            if not file_content:
                raise HTTPException(
                    status_code=400,
                    detail="Empty file"
                )

            # =========================
            # GENERATE FILE SHARE ID
            # =========================

            share_id = str(uuid.uuid4())

            # =========================
            # ENCRYPT FILE WITH METADATA
            # =========================

            encryption_result = (
                EnhancedFileEncryption
                .encrypt_file_with_metadata(
                    file_data=file_content,
                    filename=file.filename,
                    mime_type=file.content_type or "application/octet-stream",
                    password=password
                )
            )

            # =========================
            # SAVE ENCRYPTED FILE
            # =========================

            secure_filename = generate_secure_filename(
                file.filename
            )

            encrypted_file_path = (
                Path(UPLOAD_DIR)
                / f"shared_{share_id}_{secure_filename}"
            )

            await StorageManager.save_file(
                file_path=encrypted_file_path,
                content=encryption_result["encrypted_file"]
            )

            # =========================
            # GENERATE ENCRYPTION KEY FOR STORAGE
            # =========================

            encryption_key = str(uuid.uuid4())

            # =========================
            # CREATE FILE SHARE RECORD
            # =========================

            file_share = (
                FileShareRepository
                .create_file_share(
                    share_id=share_id,
                    sender_email=sender_email,
                    recipient_email=recipient_email,
                    original_filename=file.filename,
                    file_size=len(file_content),
                    mime_type=(
                        file.content_type 
                        or "application/octet-stream"
                    ),
                    file_extension=(
                        os.path.splitext(
                            file.filename
                        )[1].lower()
                    ),
                    encrypted_file_path=(
                        str(encrypted_file_path)
                    ),
                    file_checksum=(
                        encryption_result["file_checksum"]
                    ),
                    salt=(
                        encryption_result["salt"].hex()
                    ),
                    nonce=(
                        encryption_result["nonce"].hex()
                    ),
                    encryption_key=encryption_key
                )
            )

            # =========================
            # MARK SENDER VERIFIED
            # =========================

            sender_token = (
                JWTHandler.create_file_share_token(
                    share_id=share_id,
                    email=sender_email,
                    role="sender"
                )
            )

            FileShareRepository.mark_sender_verified(
                share_id,
                sender_token
            )

            return {
                "success": True,
                "message": (
                    "File encrypted and uploaded successfully"
                ),
                "share_id": share_id,
                "recipient_email": recipient_email,
                "sender_email": sender_email,
                "file_info": {
                    "filename": file.filename,
                    "size": len(file_content),
                    "mime_type": (
                        file.content_type 
                        or "application/octet-stream"
                    )
                },
                "status": "awaiting_recipient_verification"
            }

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"File encryption failed: {str(e)}"
            )

    # =========================
    # DECRYPTION PHASE
    # =========================

    @staticmethod
    async def request_decryption_access(
        request: RequestDecryptionAccessRequest
    ) -> dict:
        """
        Step 1 (Decryption): Request access to decrypt file
        Recipient initiates decryption request
        """

        try:
            # =========================
            # GET FILE SHARE
            # =========================

            file_share = (
                FileShareRepository
                .get_by_share_id(request.share_id)
            )

            if not file_share:
                raise HTTPException(
                    status_code=404,
                    detail="File share not found"
                )

            # =========================
            # VERIFY RECIPIENT
            # =========================

            if (
                file_share.recipient_email 
                != request.recipient_email
            ):
                raise HTTPException(
                    status_code=401,
                    detail="Not authorized to access this share"
                )

            # =========================
            # CHECK EXPIRATION
            # =========================

            if (
                file_share.expires_at
                and datetime.utcnow() > file_share.expires_at
            ):
                raise HTTPException(
                    status_code=410,
                    detail="File share has expired"
                )

            # =========================
            # GENERATE OTP FOR RECIPIENT
            # =========================

            recipient_otp = OTPManager.generate_otp()

            otp_session = (
                OTPSessionRepository
                .create_otp_session(
                    email=request.recipient_email,
                    otp_code=recipient_otp,
                    operation_type="decryption",
                    file_share_id=request.share_id,
                    expires_in_minutes=10
                )
            )

            # =========================
            # SEND OTP TO RECIPIENT
            # =========================

            await EmailSender.send_otp_email(
                request.recipient_email,
                recipient_otp
            )

            return {
                "success": True,
                "message": "OTP sent to recipient email",
                "session_id": otp_session.session_id,
                "recipient_email": request.recipient_email,
                "expires_in_minutes": 10
            }

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Decryption request failed: {str(e)}"
            )

    @staticmethod
    async def verify_decryption_otp(
        request: VerifyDecryptionOTPRequest,
        recipient_email: str
    ) -> dict:
        """
        Step 2 (Decryption): Verify OTP for decryption
        """

        try:
            # =========================
            # VERIFY OTP
            # =========================

            result = OTPSessionRepository.verify_otp(
                request.session_id,
                request.otp_code
            )

            if not result["success"]:
                raise HTTPException(
                    status_code=400,
                    detail=result["message"]
                )

            otp_session = result["otp_session"]

            # =========================
            # VERIFY EMAIL MATCHES
            # =========================

            if otp_session.email != recipient_email:
                raise HTTPException(
                    status_code=401,
                    detail="Email mismatch"
                )

            # =========================
            # GET FILE SHARE
            # =========================

            share_id = otp_session.file_share_id

            file_share = (
                FileShareRepository
                .get_by_share_id(share_id)
            )

            if not file_share:
                raise HTTPException(
                    status_code=404,
                    detail="File share not found"
                )

            # =========================
            # MARK RECIPIENT VERIFIED
            # =========================

            recipient_token = (
                JWTHandler.create_file_share_token(
                    share_id=share_id,
                    email=recipient_email,
                    role="recipient"
                )
            )

            FileShareRepository.mark_recipient_verified(
                share_id,
                recipient_token
            )

            return {
                "success": True,
                "message": "OTP verified. Ready to decrypt.",
                "access_token": recipient_token,
                "token_type": "bearer",
                "share_id": share_id,
                "file_info": {
                    "filename": file_share.original_filename,
                    "size": file_share.file_size,
                    "mime_type": file_share.mime_type
                }
            }

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"OTP verification failed: {str(e)}"
            )

    @staticmethod
    async def decrypt_and_download_file(
        share_id: str,
        password: str,
        recipient_email: str,
        access_token: str
    ) -> dict:
        """
        Step 3 (Decryption): Decrypt file and prepare for download
        """

        try:
            # =========================
            # VALIDATE JWT TOKEN
            # =========================

            token_result = (
                JWTHandler.verify_file_share_token(
                    access_token,
                    share_id,
                    recipient_email
                )
            )

            if not token_result["success"]:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
                )

            # =========================
            # GET FILE SHARE
            # =========================

            file_share = (
                FileShareRepository
                .get_by_share_id(share_id)
            )

            if not file_share:
                raise HTTPException(
                    status_code=404,
                    detail="File share not found"
                )

            # =========================
            # VERIFY RECIPIENT ACCESS
            # =========================

            has_access = (
                FileShareRepository
                .verify_recipient_access(
                    share_id,
                    recipient_email
                )
            )

            if not has_access:
                raise HTTPException(
                    status_code=401,
                    detail="Not authorized to access this file"
                )

            # =========================
            # READ ENCRYPTED FILE
            # =========================

            encrypted_file_path = (
                Path(file_share.encrypted_file_path)
            )

            if not encrypted_file_path.exists():
                raise HTTPException(
                    status_code=404,
                    detail="Encrypted file not found"
                )

            encrypted_content = (
                encrypted_file_path.read_bytes()
            )

            # =========================
            # DECRYPT FILE WITH METADATA
            # =========================

            decryption_result = (
                EnhancedFileEncryption
                .decrypt_file_with_metadata(
                    encrypted_data=encrypted_content,
                    password=password,
                    salt=bytes.fromhex(file_share.salt),
                    nonce=bytes.fromhex(file_share.nonce)
                )
            )

            if not decryption_result["success"]:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Decryption failed: "
                        f"{decryption_result['error']}"
                    )
                )

            file_data = decryption_result["file_data"]
            metadata = decryption_result["metadata"]

            # =========================
            # MARK AS ACCESSED
            # =========================

            FileShareRepository.mark_accessed(share_id)

            return {
                "success": True,
                "message": "File decrypted successfully",
                "share_id": share_id,
                "file_data": file_data,
                "metadata": metadata,
                "file_info": {
                    "filename": metadata["filename"],
                    "size": metadata["file_size"],
                    "mime_type": metadata["mime_type"],
                    "extension": metadata["file_extension"]
                }
            }

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"File decryption failed: {str(e)}"
            )
