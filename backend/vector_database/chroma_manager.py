import chromadb

client = chromadb.PersistentClient(
    path="./vector_database/chroma_storage"
)


class ChromaVectorDB:

    @staticmethod
    def store_embedding(

        collection_name,

        text,

        embedding,
        metadata=None
    ):

        collection = (
            client.get_or_create_collection(
                name=collection_name
            )
        )

        collection.add(

            documents=[text],

            embeddings=[embedding],

            ids=[str(hash(text))],

            metadatas=[metadata or {}]
        )

    @staticmethod
    def search(

        collection_name,

        query_embedding,

        top_k=5
    ):

        collection = (
            client.get_or_create_collection(
                name=collection_name
            )
        )

        return collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=top_k
        )