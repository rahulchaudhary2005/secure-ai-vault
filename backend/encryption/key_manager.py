import os
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives import hashes

class KeyManager:

    @staticmethod
    def generate_salt():
        return os.urandom(16)

    @staticmethod
    def derive_key(password: str, salt: bytes):

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )

        return base64.urlsafe_b64encode(
            kdf.derive(password.encode())
        )