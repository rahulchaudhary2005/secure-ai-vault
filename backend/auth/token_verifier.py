from jose import jwt
from jose import JWTError

from fastapi import HTTPException

from auth.jwt_handler import (
    SECRET_KEY,
    ALGORITHM
)


class TokenVerifier:

    @staticmethod
    def verify_token(
        token: str
    ):

        try:

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            email = payload.get("sub")

            if email is None:

                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
                )

            return email

        except JWTError:

            raise HTTPException(
                status_code=401,
                detail="Token expired or invalid"
            )