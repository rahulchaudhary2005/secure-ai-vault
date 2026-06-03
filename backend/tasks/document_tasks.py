from celery_app import celery

from storage.storage_manager import (
    StorageManager
)

from encryption.file_decryption import (
    FileDecryption
)

from ai.ocr.ocr_engine import (
    OCREngine
)

from ai.chunking.text_chunker import (
    TextChunker
)

from ai.embeddings.embedding_service import (
    EmbeddingService
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

        print("\n========== DOCUMENT TASK START ==========\n")

        print("FILE PATH:", file_path)

        print("OWNER:", owner_email)

        print("METADATA:", metadata)

        # =========================================
        # READ ENCRYPTED FILE
        # =========================================

        encrypted_content = (

            StorageManager
            .read_file_sync(file_path)
        )

        print(
            "\nEncrypted File Size:",
            len(encrypted_content)
        )

        # =========================================
        # EXTRACT SALT + NONCE
        # =========================================

        salt = bytes.fromhex(
            metadata["salt"]
        )

        nonce = bytes.fromhex(
            metadata["nonce"]
        )

        # =========================================
        # REMOVE PREFIXED SALT + NONCE
        # =========================================

        encrypted_data = (
            encrypted_content[28:]
        )

        print(
            "\nEncrypted Payload Size:",
            len(encrypted_data)
        )

        # =========================================
        # DECRYPT FILE
        # =========================================

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

        print(
            "\nDecrypted Content Size:",
            len(decrypted_content)
        )

        # =========================================
        # OCR EXTRACTION
        # =========================================

        extracted_text = (

            OCREngine.extract_text(
                decrypted_content
            )
        )

        # =========================================
        # FALLBACK TEXT DECODING
        # =========================================

        if not extracted_text:

            print(
                "\nOCR FAILED -> Using Text Decode Fallback"
            )

            extracted_text = (
                decrypted_content
                .decode(
                    errors="ignore"
                )
            )

        # =========================================
        # VALIDATE EXTRACTION
        # =========================================

        if not extracted_text:

            return {

                "success": False,

                "error":
                    "No text extracted from document."
            }

        print("\n========== OCR RESULT ==========\n")

        print(
            extracted_text[:1000]
        )

        print("\n================================\n")

        # =========================================
        # CHUNK TEXT
        # =========================================

        chunks = (

            TextChunker.chunk_text(
                extracted_text
            )
        )

        # =========================================
        # DEBUG CHUNKS
        # =========================================

        print(
            "\n========== CHUNK DEBUG ==========\n"
        )

        print(
            "TOTAL CHUNKS:",
            len(chunks)
        )

        if chunks:

            print(
                "\nFIRST CHUNK:\n"
            )

            print(
                chunks[0][:1000]
            )

        print(
            "\n=================================\n"
        )

        # =========================================
        # NO CHUNKS
        # =========================================

        if not chunks:

            return {

                "success": False,

                "error":
                    "Chunking failed."
            }

        # =========================================
        # COLLECTION NAME
        # =========================================

        collection_name = (

            owner_email
            .replace("@", "_")
            .replace(".", "_")

            + "_vault"
        )

        print(
            "\nCollection:",
            collection_name
        )

        # =========================================
        # VECTOR STORAGE
        # =========================================

        stored_chunks = 0

        for index, chunk in enumerate(chunks):

            try:

                # =====================================
                # SKIP EMPTY CHUNKS
                # =====================================

                if not chunk.strip():

                    continue

                # =====================================
                # GENERATE EMBEDDING
                # =====================================

                embedding = (

                    EmbeddingService
                    .generate_embedding(
                        chunk
                    )
                )

                print(
                    f"\nEmbedding Generated "
                    f"for Chunk {index + 1}"
                )

                # =====================================
                # SAVE VECTOR
                # =====================================

                print(
                    "\n========== VECTOR SAVE ==========\n"
                )

                print(
                    "Saving Chunk:",
                    index + 1
                )

                print(
                    "Stored Filename:",
                    metadata.get(
                        "filename",
                        ""
                    )
                )

                print(
                    "\n=================================\n"
                )

                ChromaVectorDB.store_embedding(

                    collection_name=
                        collection_name,

                    text=chunk,

                    embedding=embedding,

                    metadata={

                        # HASHED STORED FILE
                        "stored_filename":
                            metadata.get(
                                "filename",
                                ""
                            ),

                        # ORIGINAL USER FILE
                        "original_filename":
                            metadata.get(
                                "original_filename",
                                ""
                            ),

                        "mime_type":
                            metadata.get(
                                "mime_type",
                                ""
                            )
                    }
                )

                stored_chunks += 1

            except Exception as chunk_error:

                print(
                    "\nCHUNK SAVE ERROR:\n",
                    str(chunk_error)
                )

        # =========================================
        # FINAL VALIDATION
        # =========================================

        if stored_chunks == 0:

            return {

                "success": False,

                "error":
                    "No vectors stored in ChromaDB."
            }

        print(
            "\n========== DOCUMENT SUCCESS ==========\n"
        )

        print(
            "TOTAL STORED CHUNKS:",
            stored_chunks
        )

        print(
            "\n======================================\n"
        )

        # =========================================
        # SUCCESS RESPONSE
        # =========================================

        return {

            "success": True,

            "chunks_processed":
                stored_chunks
        }

    except Exception as e:

        print(
            "\n========== DOCUMENT TASK ERROR ==========\n"
        )

        print(str(e))

        print(
            "\n=========================================\n"
        )

        return {

            "success": False,

            "error": str(e)
        }