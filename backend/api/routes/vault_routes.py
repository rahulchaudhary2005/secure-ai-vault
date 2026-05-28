from fastapi import APIRouter
from fastapi import Depends

from auth.auth_guard import (
    AuthGuard
)

from database.vault_repository import (
    VaultRepository
)

router = APIRouter(
    prefix="/api/vault",
    tags=["Vault"]
)


@router.get("/documents")
async def get_user_documents(

    email: str = Depends(
        AuthGuard.protect_route
    )
):

    documents = (
        VaultRepository
        .get_user_documents(email)
    )

    return {

        "success": True,

        "total_documents": len(documents),

        "documents": [

            {

                "filename": d.original_filename,

                "encrypted_path": d.encrypted_path,

                "vector_collection": (
                    d.vector_collection
                )

            }

            for d in documents
        ]
    }