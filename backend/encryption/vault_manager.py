from backend.encryption.    FileEncryption
)

from backend.encryption.    FileDecryption
)


class VaultManager:

    @staticmethod
    def secure_encrypt_document(
        file_data: bytes,
        password: str
    ):

        encrypted = (
            FileEncryption.encrypt_file(
                file_data,
                password
            )
        )

        return encrypted

    @staticmethod
    def secure_decrypt_document(
        encrypted_data,
        password,
        salt,
        nonce
    ):

        decrypted = (
            FileDecryption.decrypt_file(
                encrypted_data,
                password,
                salt,
                nonce
            )
        )

        return decrypted