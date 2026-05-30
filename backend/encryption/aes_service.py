from cryptography.fernet import Fernet

from backend.encryption.
class AESService:

    @staticmethod
    def encrypt_data(data: bytes, password: str):

        salt = KeyManager.generate_salt()

        key = KeyManager.derive_key(password, salt)

        cipher = Fernet(key)

        encrypted = cipher.encrypt(data)

        return {
            "salt": salt,
            "encrypted_data": encrypted
        }

    @staticmethod
    def decrypt_data(
        encrypted_data: bytes,
        password: str,
        salt: bytes
    ):

        key = KeyManager.derive_key(password, salt)

        cipher = Fernet(key)

        return cipher.decrypt(encrypted_data)