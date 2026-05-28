from fastapi import APIRouter

from pydantic import BaseModel

from ai.embeddings.embedding_service import (
    EmbeddingService
)

from vector_database.chroma_manager import (
    ChromaVectorDB
)

router = APIRouter(

    prefix="/api/search",

    tags=["Semantic Search"]
)

class SearchRequest(BaseModel):

    query: str

    limit: int = 5


@router.post("/")

async def semantic_search(

    request: SearchRequest
):

    query_embedding = (

        EmbeddingService
        .generate_embedding(
            request.query
        )
    )

    results = (

        ChromaVectorDB
        .search(

            collection_name=(
                "krrahulchaudhary2005_gmail_com_vault"
            ),

            query_embedding=query_embedding,

            top_k=request.limit
        )
    )

    return {

        "success": True,

        "query": request.query,

        "results": results
    }