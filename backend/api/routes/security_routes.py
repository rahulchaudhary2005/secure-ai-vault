import base64

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from encryption.vault_manager import (
    VaultManager
)

router = APIRouter(
    prefix="/api/security",
    tags=["Security"]
)


@router.post("/encrypt")

async def encrypt_document(

    file: UploadFile = File(...),

    password: str = Form(...)
):

    content = await file.read()

    encrypted = (
        VaultManager
        .secure_encrypt_document(
            content,
            password
        )
    )

    return {

        "success": True,

        "encrypted_data": (
            base64.b64encode(
                encrypted[
                    "encrypted_data"
                ]
            ).decode()
        ),

        "salt": (
            base64.b64encode(
                encrypted["salt"]
            ).decode()
        ),

        "nonce": (
            base64.b64encode(
                encrypted["nonce"]
            ).decode()
        )
    }