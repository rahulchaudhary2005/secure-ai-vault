from cryptography.hazmat.primitives.ciphers.aead import AESGCM

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

        key = KeyManager.derive_key(
            password,
            salt
        )[:32]

        aesgcm = AESGCM(key)

        decrypted_data = aesgcm.decrypt(
            nonce,
            encrypted_data,
            None
        )

        return decrypted_data