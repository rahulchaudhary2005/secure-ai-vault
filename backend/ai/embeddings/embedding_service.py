from sentence_transformers import (
    SentenceTransformer
)

class EmbeddingService:

    model = None

    @staticmethod
    def load_model():

        if EmbeddingService.model is None:

            EmbeddingService.model = (
                SentenceTransformer(
                    "all-MiniLM-L6-v2"
                )
            )

    @staticmethod
    def generate_embedding(text):

        EmbeddingService.load_model()

        embeddings = (
            EmbeddingService
            .model
            .encode(text)
        )

        return embeddings.tolist()
    
    
    
    #.\venv\Scripts\activate