from passlib.context import CryptContext

import hashlib


pwd_context = CryptContext(
    # Use PBKDF2-SHA256 to avoid bcrypt backend issues and
    # the 72-byte input limit. PBKDF2 is widely supported
    # and requires no optional native dependencies.
    schemes=["pbkdf2_sha256"],

    deprecated="auto"
)


class PasswordManager:

    # bcrypt maximum supported length
    MAX_PASSWORD_LENGTH = 72

    @staticmethod
    def preprocess_password(
        password: str
    ) -> str:

        """
        Enterprise-safe password preprocessing.

        bcrypt supports maximum 72 bytes.

        If password exceeds limit,
        convert it into SHA256 hash first.
        """

        if not password:

            raise ValueError(
                "Password cannot be empty"
            )

        password_bytes = (
            password.encode("utf-8")
        )

        # If password too large for bcrypt
        if len(password_bytes) > (
            PasswordManager
            .MAX_PASSWORD_LENGTH
        ):

            password = hashlib.sha256(
                password_bytes
            ).hexdigest()

        return password

    @staticmethod
    def hash_password(
        password: str
    ) -> str:

        password = (
            PasswordManager
            .preprocess_password(
                password
            )
        )

        hashed_password = (
            pwd_context.hash(
                password
            )
        )

        return hashed_password

    @staticmethod
    def verify_password(

        plain_password: str,

        hashed_password: str

    ) -> bool:

        plain_password = (
            PasswordManager
            .preprocess_password(
                plain_password
            )
        )

        return pwd_context.verify(

            plain_password,

            hashed_password
        )