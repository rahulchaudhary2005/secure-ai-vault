from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/verify",
    tags=["Verification"]
)


class OTPVerifyRequest(BaseModel):

    email: str

    otp: str


@router.post("/otp")
async def verify_otp(
    request: OTPVerifyRequest
):

    return {

        "success": True,

        "message": (
            "OTP verified successfully"
        ),

        "verified_email": (
            request.email
        )
    }