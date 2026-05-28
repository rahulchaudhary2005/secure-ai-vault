from pathlib import Path
from datetime import datetime
import mimetypes
import uuid

from ai.parsers.pdf_parser import PDFParser
from ai.parsers.docx_parser import DOCXParser
from ai.parsers.pptx_parser import PPTXParser
from ai.parsers.image_parser import ImageParser
from ai.parsers.audio_parser import AudioParser
from ai.parsers.video_parser import VideoParser

from ai.chunking.text_chunker import TextChunker

from ai.embeddings.embedding_service import (
    EmbeddingService
)

from ai.vector_db.chroma_engine import (
    ChromaEngine
)


class DocumentProcessor:

    SUPPORTED_IMAGE_TYPES = [
        ".png",
        ".jpg",
        ".jpeg"
    ]

    SUPPORTED_AUDIO_TYPES = [
        ".mp3",
        ".wav"
    ]

    SUPPORTED_VIDEO_TYPES = [
        ".mp4",
        ".mov",
        ".avi"
    ]

    @staticmethod
    def process_document(

        file_path: str,

        owner_email: str

    ):

        path = Path(file_path)

        extension = path.suffix.lower()

        filename = path.name

        mime_type, _ = mimetypes.guess_type(
            str(file_path)
        )

        extracted_text = ""

        metadata = {

            "filename": filename,

            "owner_email": owner_email,

            "file_extension": extension,

            "mime_type": mime_type,

            "processed_at": (
                datetime.utcnow().isoformat()
            ),

            "ocr_processed": False,

            "audio_processed": False,

            "video_processed": False,

            "document_processed": False
        }

        # ===================================
        # PDF PROCESSING
        # ===================================

        if extension == ".pdf":

            extracted_text = (
                PDFParser.extract_text(
                    file_path
                )
            )

            metadata["document_processed"] = True

        # ===================================
        # DOCX PROCESSING
        # ===================================

        elif extension == ".docx":

            extracted_text = (
                DOCXParser.extract_text(
                    file_path
                )
            )

            metadata["document_processed"] = True

        # ===================================
        # PPTX PROCESSING
        # ===================================

        elif extension == ".pptx":

            extracted_text = (
                PPTXParser.extract_text(
                    file_path
                )
            )

            metadata["document_processed"] = True

        # ===================================
        # IMAGE OCR
        # ===================================

        elif extension in (
            DocumentProcessor
            .SUPPORTED_IMAGE_TYPES
        ):

            extracted_text = (
                ImageParser.extract_text(
                    file_path
                )
            )

            metadata["ocr_processed"] = True

        # ===================================
        # AUDIO METADATA
        # ===================================

        elif extension in (
            DocumentProcessor
            .SUPPORTED_AUDIO_TYPES
        ):

            audio_metadata = (
                AudioParser.extract_metadata(
                    file_path
                )
            )

            extracted_text = str(
                audio_metadata
            )

            metadata["audio_processed"] = True

            metadata["audio_metadata"] = (
                audio_metadata
            )

        # ===================================
        # VIDEO METADATA
        # ===================================

        elif extension in (
            DocumentProcessor
            .SUPPORTED_VIDEO_TYPES
        ):

            video_metadata = (
                VideoParser.extract_metadata(
                    file_path
                )
            )

            extracted_text = str(
                video_metadata
            )

            metadata["video_processed"] = True

            metadata["video_metadata"] = (
                video_metadata
            )

        else:

            raise ValueError(

                f"""
                Unsupported document type:
                {extension}
                """
            )

        # ===================================
        # EMPTY TEXT SAFETY
        # ===================================

        if not extracted_text:

            extracted_text = (
                "No extractable content found."
            )

        # ===================================
        # AI CHUNKING
        # ===================================

        chunks = TextChunker.chunk_text(
            extracted_text
        )

        # ===================================
        # USER VECTOR COLLECTION
        # ===================================

        secure_collection_name = (

            owner_email
            .replace("@", "_")
            .replace(".", "_")
        )

        collection_name = (
            f"{secure_collection_name}_vault"
        )

        # ===================================
        # VECTOR STORAGE
        # ===================================

        stored_vectors = 0

        for chunk in chunks:

            embedding = (
                EmbeddingService
                .generate_embedding(
                    chunk
                )
            )

            chunk_metadata = {

                "owner_email": owner_email,

                "filename": filename,

                "collection": collection_name,

                "timestamp": (
                    datetime.utcnow()
                    .isoformat()
                )
            }

            ChromaEngine.add_document(

                owner_email=owner_email,

                text=chunk,

                embedding=embedding,

                metadata=chunk_metadata
            )

            stored_vectors += 1

        # ===================================
        # AI ANALYTICS
        # ===================================

        metadata["total_characters"] = len(
            extracted_text
        )

        metadata["total_words"] = len(
            extracted_text.split()
        )

        metadata["total_chunks"] = len(
            chunks
        )

        metadata["stored_vectors"] = (
            stored_vectors
        )

        metadata["semantic_ready"] = True

        metadata["vector_db_ready"] = True

        metadata["rag_ready"] = True

        metadata["enterprise_ai_ready"] = True

        # ===================================
        # RESPONSE
        # ===================================

        return {

            "text": extracted_text,

            "chunks": chunks,

            "total_chunks": len(chunks),

            "collection_name": (
                collection_name
            ),

            "stored_vectors": (
                stored_vectors
            ),

            "metadata": metadata
        }