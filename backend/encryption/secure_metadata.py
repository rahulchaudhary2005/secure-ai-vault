import json

from encryption.    AESService
)


class SecureMetadata:

    PASSWORD = "secure_metadata_vault"

    @staticmethod
    def encrypt_metadata(
        metadata: dict
    ):

        raw_data = json.dumps(
            metadata
        ).encode()

        encrypted = (
            AESService.encrypt_data(
                raw_data,
                SecureMetadata.PASSWORD
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
                SecureMetadata.PASSWORD,
                salt
            )
        )

        return json.loads(
            decrypted.decode()
        )