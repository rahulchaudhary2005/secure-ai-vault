from fastapi import APIRouter
from fastapi import Header

from pydantic import BaseModel

from auth.token_verifier import (
    TokenVerifier
)

from database.user_repository import (
    UserRepository
)

router = APIRouter(

    prefix="/api/settings",

    tags=["Settings"]
)


class SettingsRequest(BaseModel):

    full_name: str

    role: str

    ai_model: str

    ai_temperature: str

    response_style: str

    auto_lock_minutes: int

    context_window: int

    max_response_length: int

    streaming_enabled: bool

    reasoning_enabled: bool


@router.get("/")
async def get_settings(

    authorization: str = Header(...)

):

    token = (
        authorization
        .replace("Bearer ", "")
    )

    email = (
        TokenVerifier
        .verify_token(token)
    )

    user = (
        UserRepository
        .get_settings(email)
    )

    return {

        "success": True,

        "settings": {

            "email":
                user.email,

            "full_name":
                getattr(
                    user,
                    "full_name",
                    ""
                ),

            "role":
                getattr(
                    user,
                    "role",
                    ""
                ),

            "ai_model":
                getattr(
                    user,
                    "ai_model",
                    "gemma:2b"
                ),

            "ai_temperature":
                getattr(
                    user,
                    "ai_temperature",
                    "0.3"
                ),

            "response_style":
                getattr(
                    user,
                    "response_style",
                    "professional"
                ),

            "auto_lock_minutes":
                getattr(
                    user,
                    "auto_lock_minutes",
                    15
                ),

            "context_window":
                getattr(
                    user,
                    "context_window",
                    2048
                ),

            "max_response_length":
                getattr(
                    user,
                    "max_response_length",
                    1000
                ),

            "streaming_enabled":
                getattr(
                    user,
                    "streaming_enabled",
                    True
                ),

            "reasoning_enabled":
                getattr(
                    user,
                    "reasoning_enabled",
                    False
                )
        }
    }


@router.post("/")
async def save_settings(

    request: SettingsRequest,

    authorization: str = Header(...)
):

    token = (

        authorization
        .replace(
            "Bearer ",
            ""
        )
    )

    email = (
        TokenVerifier
        .verify_token(token)
    )

    UserRepository.update_settings(

        email,

        request.dict()
    )

    return {

        "success": True,

        "message":
            "Settings updated"
    }