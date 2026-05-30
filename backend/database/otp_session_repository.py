from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal
from backend.database.models import OTPSession
import uuid


class OTPSessionRepository:
    """
    Repository for OTP Session Management
    Handles secure OTP verification for encryption/decryption
    """

    @staticmethod
    def create_otp_session(
        email: str,
        otp_code: str,
        operation_type: str,
        file_share_id: str = None,
        expires_in_minutes: int = 10
    ) -> OTPSession:
        """
        Create a new OTP session
        operation_type: "encryption", "decryption", "sender", "recipient"
        """
        
        db = SessionLocal()
        
        try:
            session_id = str(uuid.uuid4())
            
            expires_at = (
                datetime.utcnow() 
                + timedelta(minutes=expires_in_minutes)
            )

            otp_session = OTPSession(
                session_id=session_id,
                email=email,
                otp_code=otp_code,
                operation_type=operation_type,
                file_share_id=file_share_id,
                expires_at=expires_at,
                is_verified=False,
                verification_attempts=0
            )

            db.add(otp_session)
            db.commit()
            db.refresh(otp_session)
            
            return otp_session
            
        finally:
            db.close()

    @staticmethod
    def get_by_session_id(
        session_id: str
    ) -> OTPSession:
        """Retrieve OTP session by session_id"""
        
        db = SessionLocal()
        
        try:
            return db.query(OTPSession).filter(
                OTPSession.session_id == session_id
            ).first()
            
        finally:
            db.close()

    @staticmethod
    def verify_otp(
        session_id: str,
        provided_otp: str
    ) -> dict:
        """
        Verify OTP code
        Returns: {success: bool, message: str, otp_session: OTPSession or None}
        """
        
        db = SessionLocal()
        
        try:
            otp_session = db.query(OTPSession).filter(
                OTPSession.session_id == session_id
            ).first()

            if not otp_session:
                return {
                    "success": False,
                    "message": "OTP session not found"
                }

            if datetime.utcnow() > otp_session.expires_at:
                return {
                    "success": False,
                    "message": "OTP has expired"
                }

            if otp_session.is_verified:
                return {
                    "success": False,
                    "message": "OTP already verified"
                }

            if otp_session.verification_attempts >= 3:
                return {
                    "success": False,
                    "message": "Maximum verification attempts exceeded"
                }

            otp_session.verification_attempts += 1

            if otp_session.otp_code != provided_otp:
                db.commit()
                return {
                    "success": False,
                    "message": f"Invalid OTP. Attempts remaining: {3 - otp_session.verification_attempts}"
                }

            otp_session.is_verified = True
            otp_session.verified_at = datetime.utcnow()
            
            db.commit()
            db.refresh(otp_session)
            
            return {
                "success": True,
                "message": "OTP verified successfully",
                "otp_session": otp_session
            }
            
        finally:
            db.close()

    @staticmethod
    def mark_verified(
        session_id: str
    ) -> bool:
        """Mark OTP session as verified"""
        
        db = SessionLocal()
        
        try:
            otp_session = db.query(OTPSession).filter(
                OTPSession.session_id == session_id
            ).first()

            if not otp_session:
                return False

            otp_session.is_verified = True
            otp_session.verified_at = datetime.utcnow()
            
            db.commit()
            return True
            
        finally:
            db.close()

    @staticmethod
    def get_pending_sessions(
        email: str
    ) -> list:
        """Get all pending OTP sessions for an email"""
        
        db = SessionLocal()
        
        try:
            return db.query(OTPSession).filter(
                OTPSession.email == email,
                OTPSession.is_verified == False,
                OTPSession.expires_at > datetime.utcnow()
            ).all()
            
        finally:
            db.close()

    @staticmethod
    def cleanup_expired_sessions():
        """Delete expired OTP sessions"""
        
        db = SessionLocal()
        
        try:
            db.query(OTPSession).filter(
                OTPSession.expires_at <= datetime.utcnow()
            ).delete()
            
            db.commit()
            
        finally:
            db.close()

    @staticmethod
    def get_session_by_file_share(
        file_share_id: str,
        email: str,
        operation_type: str
    ) -> OTPSession:
        """Get OTP session for a specific file share"""
        
        db = SessionLocal()
        
        try:
            return db.query(OTPSession).filter(
                OTPSession.file_share_id == file_share_id,
                OTPSession.email == email,
                OTPSession.operation_type == operation_type
            ).first()
            
        finally:
            db.close()
