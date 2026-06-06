from backend.ai.vector_db.chroma_engine import (
    ChromaEngine
)

from ai.embeddings.embedding_service import (
    EmbeddingService
)

from ai.vector_db.secure_vector_store import (
    SecureVectorStore
)


class EncryptedRetriever:

    @staticmethod
    def secure_search(
        query: str,
        limit: int = 5
    ):

        query_embedding = (
            EmbeddingService
            .generate_embedding(
                query
            )
        )

        results = (
            ChromaEngine
            .semantic_search(
                query_embedding,
                limit
            )
        )

        encrypted_results = []

        documents = (
            results.get(
                "documents",
                [[]]
            )[0]
        )

        metadatas = (
            results.get(
                "metadatas",
                [[]]
            )[0]
        )

        for doc, metadata in zip(
            documents,
            metadatas
        ):

            encrypted = (
                SecureVectorStore
                .encrypt_metadata(
                    metadata
                )
            )

            encrypted_results.append({

                "document": doc,

                "encrypted_metadata": (
                    encrypted[
                        "encrypted_data"
                    ]
                    .decode()
                )
            })

        return encrypted_results