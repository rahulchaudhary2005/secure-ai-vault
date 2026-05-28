from fastapi import APIRouter

from pydantic import BaseModel

from ai.rag.rag_engine import (
    RAGEngine
)

router = APIRouter(

    prefix="/api/assistant",

    tags=["AI Assistant"]
)

class AssistantRequest(BaseModel):

    question: str


@router.post("/")

async def ai_assistant(

    request: AssistantRequest
):

    response = (

        RAGEngine.ask_question(

            question=request.question,

            owner_email=(
                "krrahulchaudhary2005@gmail.com"
            )
        )
    )

    return {

        "success": True,

        "response": response
    }