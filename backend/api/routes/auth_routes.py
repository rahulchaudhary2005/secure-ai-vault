from fastapi import APIRouter
from fastapi import HTTPException

from pydantic import BaseModel

from backend.auth.password_manager import PasswordManager
from backend.auth.email_validator import EmailValidator
from backend.auth.jwt_handler import JWTHandler
from backend.database.user_repository import UserRepository

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


class RegisterRequest(BaseModel):

    email: str

    password: str

@router.post("/register")
async def register_user(
    request: RegisterRequest
):

    valid_email = (
        EmailValidator.validate(
            request.email
        )
    )

    if not valid_email:
        raise HTTPException(
            status_code=400,
            detail="Invalid email"
        )

    existing_user = UserRepository.get_by_email(valid_email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_password = PasswordManager.hash_password(request.password)

    user = UserRepository.create_user(
        valid_email,
        hashed_password
    )

    if not user:
        raise HTTPException(
            status_code=500,
            detail="Unable to create user"
        )

    token = JWTHandler.create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "success": True,
        "message": "Registration successful",
        "user": {
            "email": user.email
        },
        "access_token": token,
        "token_type": "bearer"
    }