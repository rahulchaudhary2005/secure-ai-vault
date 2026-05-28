from fastapi import APIRouter
from fastapi import HTTPException

from pydantic import BaseModel

from auth.jwt_handler import JWTHandler
from auth.password_manager import PasswordManager
from database.user_repository import UserRepository

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login_user(
    request: LoginRequest
):

    user = UserRepository.get_by_email(request.email)

    if not user or not PasswordManager.verify_password(
        request.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = JWTHandler.create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": user.email
        }
    }