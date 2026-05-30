from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import LargeBinary
from sqlalchemy import JSON

from datetime import datetime

from backend.database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================
# ENTERPRISE VAULT MODEL
# =========================

class VaultDocument(Base):

    __tablename__ = "vault_documents"

    id = Column(
        Integer,
        primary_key=True
    )

    owner_email = Column(
        String
    )

    encrypted_path = Column(
        String
    )

    original_filename = Column(
        String
    )

    vector_collection = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
class ConversationMemory(Base):

    __tablename__ = "conversation_memory"

    id = Column(
        Integer,
        primary_key=True
    )

    owner_email = Column(
        String
    )

    user_message = Column(
        String
    )

    ai_response = Column(
        String
    )

    semantic_tag = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================
# SECURE FILE SHARING MODEL
# =========================

class FileShare(Base):
    """
    Industry-Grade Secure File Sharing Model
    Tracks sender, recipient, encryption keys, and OTP verification
    """
    
    __tablename__ = "file_shares"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    share_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    sender_email = Column(
        String,
        nullable=False,
        index=True
    )

    recipient_email = Column(
        String,
        nullable=False,
        index=True
    )

    original_filename = Column(
        String,
        nullable=False
    )

    file_size = Column(
        Integer,
        nullable=False
    )

    mime_type = Column(
        String,
        nullable=False
    )

    file_extension = Column(
        String,
        nullable=False
    )

    encrypted_file_path = Column(
        String,
        nullable=False
    )

    file_checksum = Column(
        String,
        nullable=False
    )

    salt = Column(
        String,
        nullable=False
    )

    nonce = Column(
        String,
        nullable=False
    )

    encryption_key = Column(
        String,
        nullable=False
    )

    sender_otp_verified = Column(
        Boolean,
        default=False
    )

    recipient_otp_verified = Column(
        Boolean,
        default=False
    )

    sender_access_token = Column(
        String,
        nullable=True
    )

    recipient_access_token = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        default="pending",
        nullable=False
    )

    # 'metadata' is a reserved attribute name on the Declarative base
    # use a different attribute name while keeping the DB column name
    # as 'metadata' so existing DB layout and API keys remain unchanged.
    metadata_json = Column(
        'metadata',
        JSON,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    expires_at = Column(
        DateTime,
        nullable=True
    )

    accessed_at = Column(
        DateTime,
        nullable=True
    )


# =========================
# OTP SESSION MODEL
# =========================

class OTPSession(Base):
    """
    Manages OTP verification for secure file sharing
    """
    
    __tablename__ = "otp_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String,
        nullable=False,
        index=True
    )

    otp_code = Column(
        String,
        nullable=False
    )

    operation_type = Column(
        String,
        nullable=False
    )

    file_share_id = Column(
        String,
        nullable=True
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    verification_attempts = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    verified_at = Column(
        DateTime,
        nullable=True
    )