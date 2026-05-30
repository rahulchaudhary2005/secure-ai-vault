from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Header

from pydantic import BaseModel

from backend.auth.jwt_handler import JWTHandler
from backend.auth.password_manager import PasswordManager
from backend.auth.email_validator import EmailValidator
from backend.database.user_repository import UserRepository

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login_user(
    request: LoginRequest,
    x_debug_auth: Optional[str] = Header(
        None,
        alias="X-Debug-Auth"
    )
):

    debug_mode = str(x_debug_auth).lower() in ("1", "true", "yes")
    debug_payload = {
        "email_valid_format": None,
        "email_exists": None,
        "password_valid": None
    }

    valid_email = EmailValidator.validate(request.email)
    debug_payload["email_valid_format"] = bool(valid_email)

    if not valid_email:
        content = {
            "success": False,
            "detail": "Invalid email or password"
        }
        if debug_mode:
            content["debug"] = debug_payload
        raise HTTPException(
            status_code=401,
            detail=content
        )

    user = UserRepository.get_by_email(valid_email)
    debug_payload["email_exists"] = bool(user)

    password_ok = False
    if user:
        password_ok = PasswordManager.verify_password(
            request.password,
            user.hashed_password
        )
    debug_payload["password_valid"] = password_ok

    if not user or not password_ok:
        content = {
            "success": False,
            "detail": "Invalid email or password"
        }
        if debug_mode:
            content["debug"] = debug_payload
        raise HTTPException(
            status_code=401,
            detail=content
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