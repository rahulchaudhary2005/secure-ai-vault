from fastapi import APIRouter

from pydantic import BaseModel
from typing import List, Optional

from ai.rag.rag_engine import (
    RAGEngine
)

router = APIRouter(

    prefix="/api/chat",

    tags=["AI Chat"]
)

class ChatRequest(BaseModel):

    question: str
    files: Optional[List[str]] = None


@router.post("/")

async def chat_with_ai(

    request: ChatRequest
):

    response = (

        RAGEngine.ask_question(

            question=request.question,
            owner_email=(
                "krrahulchaudhary2005@gmail.com"
            ),
            filenames=request.files
        )
    )

    return {

        "success": True,

        "response": response
    }