from cryptography.hazmat.primitives.ciphers.aead import (
    AESGCM
)

from encryption.key_manager import (
    KeyManager
)


class FileDecryption:

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