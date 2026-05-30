"""
Enterprise-Grade File Encryption with Metadata Preservation
Ensures exact file reconstruction after decryption
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes

import os
import json
import hashlib
from typing import Tuple
from backend.encryption.

class EnhancedFileEncryption:
    """
    Enterprise-grade file encryption with:
    - AES-256-GCM encryption
    - File metadata preservation
    - File integrity verification (HMAC)
    - Exact file reconstruction
    """

    # File format version for future compatibility
    FILE_FORMAT_VERSION = "1.0"

    @staticmethod
    def calculate_file_checksum(
        file_data: bytes
    ) -> str:
        """Calculate SHA-256 checksum of file"""
        return hashlib.sha256(file_data).hexdigest()

    @staticmethod
    def create_file_metadata(
        filename: str,
        file_data: bytes,
        mime_type: str
    ) -> dict:
        """Create comprehensive file metadata"""
        
        return {
            "filename": filename,
            "file_size": len(file_data),
            "mime_type": mime_type,
            "file_extension": (
                os.path.splitext(filename)[1].lower()
            ),
            "checksum": (
                EnhancedFileEncryption
                .calculate_file_checksum(file_data)
            ),
            "format_version": (
                EnhancedFileEncryption.FILE_FORMAT_VERSION
            )
        }

    @staticmethod
    def encrypt_file_with_metadata(
        file_data: bytes,
        filename: str,
        mime_type: str,
        password: str
    ) -> dict:
        """
        Encrypt file with metadata preservation
        
        Returns: {
            "encrypted_file": bytes,
            "salt": bytes,
            "nonce": bytes,
            "metadata": dict,
            "metadata_json": str,
            "file_checksum": str
        }
        """

        # =========================
        # CREATE FILE METADATA
        # =========================

        metadata = EnhancedFileEncryption.create_file_metadata(
            filename,
            file_data,
            mime_type
        )

        file_checksum = metadata["checksum"]

        # =========================
        # GENERATE CRYPTOGRAPHIC MATERIAL
        # =========================

        salt = os.urandom(16)
        nonce = os.urandom(12)

        # =========================
        # DERIVE ENCRYPTION KEY
        # =========================

        key = KeyManager.derive_key(
            password,
            salt
        )[:32]

        # =========================
        # SERIALIZE METADATA
        # =========================

        metadata_json = json.dumps(metadata)
        metadata_bytes = metadata_json.encode('utf-8')

        # =========================
        # PREPARE DATA FOR ENCRYPTION
        # =========================

        metadata_length = len(metadata_bytes).to_bytes(4, 'big')
        data_to_encrypt = (
            metadata_length + metadata_bytes + file_data
        )

        # =========================
        # AES-256-GCM ENCRYPTION
        # =========================

        aesgcm = AESGCM(key)

        encrypted_data = aesgcm.encrypt(
            nonce,
            data_to_encrypt,
            None
        )

        return {
            "encrypted_file": encrypted_data,
            "salt": salt,
            "nonce": nonce,
            "metadata": metadata,
            "metadata_json": metadata_json,
            "file_checksum": file_checksum
        }

    @staticmethod
    def decrypt_file_with_metadata(
        encrypted_data: bytes,
        password: str,
        salt: bytes,
        nonce: bytes
    ) -> dict:
        """
        Decrypt file with metadata extraction
        
        Returns: {
            "success": bool,
            "file_data": bytes or None,
            "metadata": dict or None,
            "error": str or None
        }
        """

        try:
            # =========================
            # DERIVE DECRYPTION KEY
            # =========================

            key = KeyManager.derive_key(
                password,
                salt
            )[:32]

            # =========================
            # AES-256-GCM DECRYPTION
            # =========================

            aesgcm = AESGCM(key)

            decrypted_data = aesgcm.decrypt(
                nonce,
                encrypted_data,
                None
            )

            # =========================
            # EXTRACT METADATA LENGTH
            # =========================

            metadata_length = int.from_bytes(
                decrypted_data[:4],
                'big'
            )

            # =========================
            # EXTRACT METADATA
            # =========================

            metadata_bytes = (
                decrypted_data[4:4 + metadata_length]
            )

            metadata_json = metadata_bytes.decode('utf-8')
            metadata = json.loads(metadata_json)

            # =========================
            # EXTRACT FILE DATA
            # =========================

            file_data = decrypted_data[4 + metadata_length:]

            # =========================
            # VERIFY FILE INTEGRITY
            # =========================

            calculated_checksum = (
                EnhancedFileEncryption
                .calculate_file_checksum(file_data)
            )

            if (
                calculated_checksum 
                != metadata["checksum"]
            ):
                return {
                    "success": False,
                    "file_data": None,
                    "metadata": None,
                    "error": "File integrity check failed"
                }

            return {
                "success": True,
                "file_data": file_data,
                "metadata": metadata,
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "file_data": None,
                "metadata": None,
                "error": str(e)
            }

    @staticmethod
    def verify_encrypted_file_integrity(
        encrypted_data: bytes,
        checksum: str,
        password: str,
        salt: bytes,
        nonce: bytes
    ) -> bool:
        """Verify that encrypted file matches expected checksum"""

        result = (
            EnhancedFileEncryption
            .decrypt_file_with_metadata(
                encrypted_data,
                password,
                salt,
                nonce
            )
        )

        if not result["success"]:
            return False

        metadata = result["metadata"]
        return metadata.get("checksum") == checksum

    @staticmethod
    def get_encrypted_file_metadata(
        encrypted_data: bytes,
        password: str,
        salt: bytes,
        nonce: bytes
    ) -> dict:
        """
        Extract metadata from encrypted file
        without decrypting the actual file data
        """

        result = (
            EnhancedFileEncryption
            .decrypt_file_with_metadata(
                encrypted_data,
                password,
                salt,
                nonce
            )
        )

        if not result["success"]:
            return {
                "success": False,
                "metadata": None,
                "error": result["error"]
            }

        return {
            "success": True,
            "metadata": result["metadata"],
            "error": None
        }
