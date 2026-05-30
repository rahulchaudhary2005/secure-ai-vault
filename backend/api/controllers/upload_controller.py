from pathlib import Path
from datetime import datetime
import hashlib
import mimetypes

from fastapi import UploadFile
from fastapi import HTTPException

from utils.constants import UPLOAD_DIR

from storage.storage_manager import (
    StorageManager
)

from utils.helpers import (
    validate_file_extension,
    generate_secure_filename
)

from backend.database.vault_repository import (
    VaultRepository
)

from tasks.document_tasks import (
    process_document_task
)

from encryption.file_encryption import (
    FileEncryption
)


class UploadController:

    MAX_FILE_SIZE = 1024 * 1024 * 200

    @staticmethod
    async def upload_document(
        file: UploadFile
    ):

        try:

            if not file:

                raise HTTPException(
                    status_code=400,
                    detail="No file uploaded"
                )

            validate_file_extension(
                file.filename
            )

            secure_filename = (
                generate_secure_filename(
                    file.filename
                )
            )

            file_path = (
                Path(UPLOAD_DIR)
                / secure_filename
            )

            content = await file.read()

            if len(content) > UploadController.MAX_FILE_SIZE:

                raise HTTPException(
                    status_code=413,
                    detail="File exceeds 200MB limit"
                )

            mime_type, _ = mimetypes.guess_type(
                file.filename
            )

            sha256_hash = hashlib.sha256(
                content
            ).hexdigest()

            encrypted = FileEncryption.encrypt_file(

                file_data=content,

                password="enterprise_secure_password"
            )

            encrypted_content = (

                encrypted["salt"] +

                encrypted["nonce"] +

                encrypted["encrypted_data"]
            )

            await StorageManager.save_file(

                file_path=file_path,

                content=encrypted_content
            )

            owner_email = (
                "krrahulchaudhary2005@gmail.com"
            )

            metadata = {

                "filename": secure_filename,

                "original_filename":
                    file.filename,

                "mime_type":
                    mime_type,

                "size_bytes":
                    len(content),

                "sha256":
                    sha256_hash,

                "uploaded_at":
                    datetime.utcnow().isoformat(),

                "salt":
                    encrypted["salt"].hex(),

                "nonce":
                    encrypted["nonce"].hex()
            }

            VaultRepository.save_document(

                owner_email=owner_email,

                encrypted_path=str(file_path),

                original_filename=file.filename,

                vector_collection=(

                    f"{owner_email}"
                    .replace("@", "_")
                    .replace(".", "_")

                    + "_vault"
                )
            )

            task = process_document_task.delay(

                str(file_path),

                owner_email,

                metadata
            )

            return {

                "success": True,

                "task_id": task.id,

                "message":
                    "Encrypted document uploaded successfully",

                "document": metadata
            }

        except HTTPException as e:

            raise e

        except Exception as e:

            raise HTTPException(

                status_code=500,

                detail=f"""

                Enterprise AI upload pipeline failed:

                {str(e)}

                """
            )

    @staticmethod
    async def list_uploaded_files():

        upload_path = Path(UPLOAD_DIR)

        if not upload_path.exists():
            return {
                "success": True,
                "files": []
            }

        files = []

        for file_path in upload_path.iterdir():
            if file_path.is_file():
                files.append({
                    "filename": file_path.name,
                    "size_bytes": file_path.stat().st_size,
                    "uploaded_at": datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    ).isoformat()
                })

        return {
            "success": True,
            "files": files
        }

    @staticmethod
    async def upload_documents(
        files
    ):

        uploaded_files = []

        for file in files:

            response = (
                await UploadController
                .upload_document(file)
            )

            uploaded_files.append({

                "filename":
                    file.filename,

                "status":
                    "uploaded",

                "task_id":
                    response.get("task_id")
            })

        return {

            "success": True,

            "message":
                "Secure files uploaded successfully",

            "files":
                uploaded_files
        }