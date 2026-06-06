import json

from encryption.aes_service import AESService

class SecureVectorStore:

    PASSWORD = "secure_ai_vault"

    @staticmethod
    def encrypt_metadata(metadata: dict):

        raw_data = json.dumps(
            metadata
        ).encode()

        encrypted = (
            AESService.encrypt_data(
                raw_data,
                SecureVectorStore.PASSWORD
            )
        )

        return encrypted

    @staticmethod
    def decrypt_metadata(
        encrypted_data,
        salt
    ):

        decrypted = (
            AESService.decrypt_data(
                encrypted_data,
                SecureVectorStore.PASSWORD,
                salt
            )
        )

        return json.loads(
            decrypted.decode()
        )