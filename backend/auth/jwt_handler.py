from datetime import datetime
from datetime import timedelta
from jose import jwt
from jose.exceptions import JWTError


# =========================
# SECURITY CONFIGURATION
# =========================

SECRET_KEY = (
    "SUPER_SECURE_AI_VAULT_SECRET_KEY_2026"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

FILE_SHARE_TOKEN_EXPIRE_MINUTES = 120

REFRESH_TOKEN_EXPIRE_DAYS = 7


class JWTHandler:

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: timedelta = None
    ):
        """
        Create standard access token
        """

        to_encode = data.copy()

        if expires_delta:
            expire = (
                datetime.utcnow() + expires_delta
            )
        else:
            expire = (
                datetime.utcnow()
                + timedelta(
                    minutes=(
                        ACCESS_TOKEN_EXPIRE_MINUTES
                    )
                )
            )

        to_encode.update({
            "exp": expire,
            "type": "access"
        })

        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def create_file_share_token(
        share_id: str,
        email: str,
        role: str,
        expires_delta: timedelta = None
    ):
        """
        Create specialized token for file sharing
        role: "sender" or "recipient"
        """

        data = {
            "share_id": share_id,
            "email": email,
            "role": role,
            "type": "file_share"
        }

        to_encode = data.copy()

        if expires_delta:
            expire = (
                datetime.utcnow() + expires_delta
            )
        else:
            expire = (
                datetime.utcnow()
                + timedelta(
                    minutes=(
                        FILE_SHARE_TOKEN_EXPIRE_MINUTES
                    )
                )
            )

        to_encode.update({
            "exp": expire
        })

        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def create_refresh_token(
        email: str
    ):
        """
        Create refresh token for session management
        """

        data = {
            "sub": email,
            "type": "refresh"
        }

        to_encode = data.copy()

        expire = (
            datetime.utcnow()
            + timedelta(
                days=REFRESH_TOKEN_EXPIRE_DAYS
            )
        )

        to_encode.update({
            "exp": expire
        })

        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def verify_token(
        token: str
    ):
        """
        Verify and decode JWT token
        Returns: {success: bool, payload: dict or None, error: str or None}
        """

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            return {
                "success": True,
                "payload": payload,
                "error": None
            }

        except JWTError as e:
            return {
                "success": False,
                "payload": None,
                "error": str(e)
            }

    @staticmethod
    def verify_file_share_token(
        token: str,
        share_id: str,
        email: str
    ):
        """
        Verify file share token with specific claims
        """

        result = JWTHandler.verify_token(token)

        if not result["success"]:
            return result

        payload = result["payload"]

        if (
            payload.get("share_id") != share_id
            or payload.get("email") != email
            or payload.get("type") != "file_share"
        ):
            return {
                "success": False,
                "payload": None,
                "error": "Invalid file share token claims"
            }

        return result

    @staticmethod
    def extract_email_from_token(
        token: str
    ):
        """
        Extract email from token
        Returns: email or None
        """

        result = JWTHandler.verify_token(token)

        if not result["success"]:
            return None

        payload = result["payload"]
        return payload.get("sub") or payload.get("email")

    @staticmethod
    def extract_share_id_from_token(
        token: str
    ):
        """
        Extract share_id from file share token
        """

        result = JWTHandler.verify_token(token)

        if not result["success"]:
            return None

        payload = result["payload"]
        return payload.get("share_id")