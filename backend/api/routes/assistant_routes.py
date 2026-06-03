from fastapi import APIRouter

from pydantic import BaseModel

from ai.rag.rag_engine import (
    RAGEngine
)

from ai.langchain.ollama_engine import (
    OllamaEngine
)

router = APIRouter(

    prefix="/api/assistant",

    tags=["AI Assistant"]
)


# =====================================
# REQUEST MODEL
# =====================================

class AssistantRequest(
    BaseModel
):

    question: str


# =====================================
# SIMPLE CHAT DETECTION
# =====================================

def is_general_chat(
    question: str
):

    q = question.lower().strip()

    general_words = [

        "hi",
        "hii",
        "hello",
        "hey",
        "how are you",
        "good morning",
        "good evening",
        "who are you"
    ]

    return q in general_words


# =====================================
# AI ASSISTANT ROUTE
# =====================================

@router.post("/")
async def ai_assistant(

    request: AssistantRequest
):

    try:

        question = (
            request.question.strip()
        )

        if not question:

            return {

                "success": False,

                "answer":
                    "Question cannot be empty."
            }

        # =====================================
        # FAST GENERAL CHAT
        # =====================================

        if is_general_chat(question):

            response = (
                OllamaEngine
                .generate_response(
                    question
                )
            )

            return {

                "success": True,

                "intent": "general_chat",

                "answer": response
            }

        # =====================================
        # RAG DOCUMENT QUERY
        # =====================================

        response = (

            RAGEngine.ask_question(

                question=question,

                owner_email=(
                    "krrahulchaudhary2005@gmail.com"
                )
            )
        )

        if isinstance(response, dict):

            return {

                "success": True,

                "intent": "rag_query",

                "answer": (

                    response.get("answer")

                    or "No response generated."
                )
            }

        return {

            "success": True,

            "intent": "rag_query",

            "answer": str(response)
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }