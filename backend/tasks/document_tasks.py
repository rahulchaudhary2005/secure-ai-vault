from celery_app import celery

from backend.storage.    StorageManager
)

from backend.encryption.    FileDecryption
)

from backend.ai.    OCREngine
)

from backend.ai.    TextChunker
)

from backend.ai.    EmbeddingService
)

from vector_database.chroma_manager import (
    ChromaVectorDB
)


@celery.task
def process_document_task(

    file_path,

    owner_email,

    metadata
):

    try:

        encrypted_content = (

            StorageManager
            .read_file_sync(file_path)
        )

        salt = bytes.fromhex(
            metadata["salt"]
        )

        nonce = bytes.fromhex(
            metadata["nonce"]
        )

        encrypted_data = (
            encrypted_content[28:]
        )

        decrypted_content = (

            FileDecryption.decrypt_file(

                encrypted_data=
                    encrypted_data,

                password=(
                    "enterprise_secure_password"
                ),

                salt=salt,

                nonce=nonce
            )
        )

        extracted_text = (

            OCREngine.extract_text(
                decrypted_content
            )
        )

        if not extracted_text:

            extracted_text = (
                decrypted_content
                .decode(
                    errors="ignore"
                )
            )

        chunks = (

            TextChunker.chunk_text(
                extracted_text
            )
        )

        collection_name = (

            owner_email
            .replace("@", "_")
            .replace(".", "_")

            + "_vault"
        )

        for chunk in chunks:

            embedding = (

                EmbeddingService
                .generate_embedding(
                    chunk
                )
            )

            ChromaVectorDB.store_embedding(

                collection_name=
                    collection_name,

                text=chunk,

                embedding=embedding,

                metadata={
                    "source_filename":
                        metadata.get("filename"),

                    "original_filename":
                        metadata.get("original_filename")
                }
            )

        return {

            "success": True,

            "chunks_processed":
                len(chunks)
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }