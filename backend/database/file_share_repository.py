from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.models import FileShare


class FileShareRepository:
    """
    Repository for File Sharing Operations
    Industry-grade secure file access control
    """

    @staticmethod
    def create_file_share(
        share_id: str,
        sender_email: str,
        recipient_email: str,
        original_filename: str,
        file_size: int,
        mime_type: str,
        file_extension: str,
        encrypted_file_path: str,
        file_checksum: str,
        salt: str,
        nonce: str,
        encryption_key: str,
        expires_in_hours: int = 48
    ) -> FileShare:
        """Create a new file share record"""
        
        db = SessionLocal()
        
        try:
            expires_at = (
                datetime.utcnow() 
                + timedelta(hours=expires_in_hours)
            )

            file_share = FileShare(
                share_id=share_id,
                sender_email=sender_email,
                recipient_email=recipient_email,
                original_filename=original_filename,
                file_size=file_size,
                mime_type=mime_type,
                file_extension=file_extension,
                encrypted_file_path=encrypted_file_path,
                file_checksum=file_checksum,
                salt=salt,
                nonce=nonce,
                encryption_key=encryption_key,
                status="pending",
                expires_at=expires_at,
                metadata_json={
                    "created_by_user": sender_email,
                    "shared_with": recipient_email
                }
            )

            db.add(file_share)
            db.commit()
            db.refresh(file_share)
            
            return file_share
            
        finally:
            db.close()

    @staticmethod
    def get_by_share_id(
        share_id: str
    ) -> FileShare:
        """Retrieve file share by share_id"""
        
        db = SessionLocal()
        
        try:
            return db.query(FileShare).filter(
                FileShare.share_id == share_id
            ).first()
            
        finally:
            db.close()

    @staticmethod
    def mark_sender_verified(
        share_id: str,
        access_token: str
    ) -> bool:
        """Mark sender OTP as verified"""
        
        db = SessionLocal()
        
        try:
            file_share = db.query(FileShare).filter(
                FileShare.share_id == share_id
            ).first()

            if not file_share:
                return False

            file_share.sender_otp_verified = True
            file_share.sender_access_token = access_token
            
            if (file_share.recipient_otp_verified):
                file_share.status = "active"

            db.commit()
            return True
            
        finally:
            db.close()

    @staticmethod
    def mark_recipient_verified(
        share_id: str,
        access_token: str
    ) -> bool:
        """Mark recipient OTP as verified"""
        
        db = SessionLocal()
        
        try:
            file_share = db.query(FileShare).filter(
                FileShare.share_id == share_id
            ).first()

            if not file_share:
                return False

            file_share.recipient_otp_verified = True
            file_share.recipient_access_token = access_token
            
            if (file_share.sender_otp_verified):
                file_share.status = "active"

            db.commit()
            return True
            
        finally:
            db.close()

    @staticmethod
    def mark_accessed(
        share_id: str
    ) -> bool:
        """Mark file as accessed"""
        
        db = SessionLocal()
        
        try:
            file_share = db.query(FileShare).filter(
                FileShare.share_id == share_id
            ).first()

            if not file_share:
                return False

            file_share.accessed_at = datetime.utcnow()
            file_share.status = "accessed"
            
            db.commit()
            return True
            
        finally:
            db.close()

    @staticmethod
    def get_user_shares(
        email: str,
        role: str = "recipient"
    ) -> list:
        """Get all shares for a user (as recipient or sender)"""
        
        db = SessionLocal()
        
        try:
            if role == "recipient":
                return db.query(FileShare).filter(
                    FileShare.recipient_email == email,
                    FileShare.status.in_(["active", "accessed"])
                ).all()
            else:
                return db.query(FileShare).filter(
                    FileShare.sender_email == email
                ).all()
                
        finally:
            db.close()

    @staticmethod
    def verify_recipient_access(
        share_id: str,
        recipient_email: str
    ) -> bool:
        """Verify that recipient can access this share"""
        
        db = SessionLocal()
        
        try:
            file_share = db.query(FileShare).filter(
                FileShare.share_id == share_id
            ).first()

            if not file_share:
                return False

            return (
                file_share.recipient_email == recipient_email
                and file_share.recipient_otp_verified
                and file_share.status in ["active", "accessed"]
            )
            
        finally:
            db.close()

    @staticmethod
    def update_metadata(
        share_id: str,
        metadata_dict: dict
    ) -> bool:
        """Update file share metadata"""
        
        db = SessionLocal()
        
        try:
            file_share = db.query(FileShare).filter(
                FileShare.share_id == share_id
            ).first()

            if not file_share:
                return False

            if file_share.metadata_json is None:
                file_share.metadata_json = {}

            file_share.metadata_json.update(metadata_dict)
            
            db.commit()
            return True
            
        finally:
            db.close()
