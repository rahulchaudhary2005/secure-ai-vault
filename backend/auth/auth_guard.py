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

            token = credentials.credentials

            email = (
                TokenVerifier
                .verify_token(token)
            )

            return email

        except Exception:

            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )