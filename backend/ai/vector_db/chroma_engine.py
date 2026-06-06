import uuid
import chromadb

from chromadb.config import (
    Settings
)


class ChromaEngine:

    # ===================================
    # PERSISTENT VECTOR DATABASE
    # ===================================

    client = chromadb.PersistentClient(

        path="./vector_database",

        settings=Settings(

            anonymized_telemetry=False
        )
    )

    # ===================================
    # USER COLLECTION
    # ===================================

    @staticmethod
    def get_user_collection(
        owner_email: str
    ):

        secure_collection_name = (

            owner_email
            .replace("@", "_")
            .replace(".", "_")
        )

        collection_name = (
            f"{secure_collection_name}_vault"
        )

        collection = (

            ChromaEngine.client
            .get_or_create_collection(
                name=collection_name
            )
        )

        return collection

    # ===================================
    # ADD DOCUMENT
    # ===================================

    @staticmethod
    def add_document(

        owner_email: str,

        text: str,

        embedding,

        metadata=None
    ):

        collection = (

            ChromaEngine
            .get_user_collection(
                owner_email
            )
        )

        document_id = str(
            uuid.uuid4()
        )

        collection.add(

            ids=[document_id],

            documents=[text],

            embeddings=[embedding],

            metadatas=[metadata or {}]
        )

        return {

            "success": True,

            "document_id": document_id,

            "collection": collection.name
        }

    # ===================================
    # SEMANTIC SEARCH
    # ===================================

    @staticmethod
    def semantic_search(

        owner_email: str,

        query_embedding,

        limit=3,

        metadata_filter: dict = None
    ):

        collection = (

            ChromaEngine
            .get_user_collection(
                owner_email
            )
        )

        query_kwargs = {

            "query_embeddings":
                [query_embedding],

            "n_results":
                limit
        }

        if metadata_filter:

            query_kwargs["where"] = (
                metadata_filter
            )

        results = (
            collection.query(
                **query_kwargs
            )
        )

        return results

    # ===================================
    # COLLECTION STATS
    # ===================================

    @staticmethod
    def get_collection_stats(
        owner_email: str
    ):

        collection = (

            ChromaEngine
            .get_user_collection(
                owner_email
            )
        )

        return {

            "collection_name":
                collection.name,

            "total_vectors":
                collection.count()
        }

    # ===================================
    # DELETE COLLECTION
    # ===================================

    @staticmethod
    def delete_user_collection(
        owner_email: str
    ):

        secure_collection_name = (

            owner_email
            .replace("@", "_")
            .replace(".", "_")
        )

        collection_name = (
            f"{secure_collection_name}_vault"
        )

        ChromaEngine.client.delete_collection(
            name=collection_name
        )

        return {

            "success": True,

            "deleted_collection":
                collection_name
        }

    # ===================================
    # LIST COLLECTIONS
    # ===================================

    @staticmethod
    def list_collections():

        collections = (

            ChromaEngine.client
            .list_collections()
        )

        return [

            collection.name

            for collection in collections
        ]