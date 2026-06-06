from fastapi import APIRouter
from fastapi import Depends

from pydantic import BaseModel
from typing import List, Optional

from auth.auth_guard import (
    AuthGuard
)

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

    request: ChatRequest,

    email: str = Depends(
        AuthGuard.protect_route
    )
):

    response = (

        RAGEngine.ask_question(

            question=request.question,

            owner_email=email,

            filenames=request.files
        )
    )

    return {

        "success": True,

        "response": response
    }