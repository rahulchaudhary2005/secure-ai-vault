from fastapi import APIRouter
from fastapi import Depends

from backend.auth.auth_guard import (
    AuthGuard
)

router = APIRouter(
    prefix="/api/protected",
    tags=["Protected"]
)


@router.get("/vault")
async def protected_vault(
    email: str = Depends(
        AuthGuard.protect_route
    )
):

    return {

        "success": True,

        "message": (
            "Access granted"
        ),

        "vault_owner": email
    }