from encryption.file_encryption import (
    FileEncryption
)

from encryption.file_decryption import (
    FileDecryption
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