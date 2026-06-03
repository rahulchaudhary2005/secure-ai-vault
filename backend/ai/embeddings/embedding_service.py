class EmbeddingService:

    model = None

    @staticmethod
    def load_model():

        if EmbeddingService.model is None:

            from sentence_transformers import (
                SentenceTransformer
            )

            # ===================================
            # FAST EMBEDDING MODEL
            # ===================================

            EmbeddingService.model = (

                SentenceTransformer(
                    "all-MiniLM-L6-v2",
                    device="cpu"
                )
            )

    @staticmethod
    def generate_embedding(text):

        EmbeddingService.load_model()

        embeddings = (

            EmbeddingService
            .model
            .encode(
                text,
                normalize_embeddings=True
            )
        )

        return embeddings.tolist()