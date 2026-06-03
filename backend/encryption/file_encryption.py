from cryptography.hazmat.primitives.ciphers.aead import (
    AESGCM
)

import os

from encryption.key_manager import (
    KeyManager
)


class FileEncryption:

    @staticmethod
    def encrypt_file(

        file_data: bytes,

        password: str
    ):

        # =========================
        # GENERATE SALT
        # =========================

        salt = os.urandom(16)

        # =========================
        # DERIVE KEY
        # =========================

        key = KeyManager.derive_key(

            password,

            salt
        )[:32]

        # =========================
        # GENERATE NONCE
        # =========================

        nonce = os.urandom(12)

        # =========================
        # AES GCM
        # =========================

        aesgcm = AESGCM(key)

        encrypted_data = aesgcm.encrypt(

            nonce,

            file_data,

            None
        )

        return {

            "encrypted_data":
                encrypted_data,

            "salt":
                salt,

            "nonce":
                nonce
        }

    @staticmethod
    def decrypt_file(

        encrypted_data: bytes,

        password: str,

        salt: bytes,

        nonce: bytes
    ):

        # =========================
        # DERIVE SAME KEY
        # =========================

        key = KeyManager.derive_key(

            password,

            salt
        )[:32]

        # =========================
        # AES GCM DECRYPTION
        # =========================

        aesgcm = AESGCM(key)

        decrypted = aesgcm.decrypt(

            nonce,

            encrypted_data,

            None
        )

        return decrypted