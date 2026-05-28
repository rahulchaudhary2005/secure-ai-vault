import base64

from fastapi import (
    APIRouter,
    HTTPException
)

from pydantic import BaseModel

from encryption.vault_manager import (
    VaultManager
)

router = APIRouter(

    prefix="/api/decrypt",

    tags=["Decryption"]
)

class DecryptRequest(BaseModel):

    encrypted_data: str

    salt: str

    nonce: str

    password: str


@router.post("/")

async def decrypt_document(

    request: DecryptRequest
):

    try:

        decrypted = (

            VaultManager
            .secure_decrypt_document(

                encrypted_data=(

                    base64.b64decode(
                        request.encrypted_data
                    )
                ),

                password=request.password,

                salt=(

                    bytes.fromhex(
                        request.salt
                    )
                ),

                nonce=(

                    bytes.fromhex(
                        request.nonce
                    )
                )
            )
        )

        return {

            "success": True,

            "message":
                "Document decrypted successfully",

            "decrypted_size":
                len(decrypted)
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"""

            Secure decrypt failed:

            {str(e)}

            """
        )