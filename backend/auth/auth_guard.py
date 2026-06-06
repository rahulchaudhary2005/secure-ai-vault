from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends

from auth.token_verifier import (
    TokenVerifier
)

security = HTTPBearer()


class AuthGuard:

    @staticmethod
    async def protect_route(

        credentials: HTTPAuthorizationCredentials = Depends(security)

    ):

        try:

            print("\n========== AUTH DEBUG ==========")
            print("Credentials:", credentials)
            print("Token:", credentials.credentials[:50] if credentials else None)

            token = credentials.credentials

            email = (
                TokenVerifier
                .verify_token(token)
            )

            print("Authenticated Email:", email)
            print("================================\n")

            return email

        except Exception as e:

            print("\n========== AUTH ERROR ==========")
            print(str(e))
            print("================================\n")

            raise HTTPException(
                status_code=401,
                detail=str(e)
            )