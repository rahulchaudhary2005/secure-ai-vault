from fastapi import APIRouter

from backend.database.database import SessionLocal
from backend.database.models import VaultDocument
from backend.database.models import ConversationMemory

router = APIRouter()


@router.get("/api/dashboard/stats")
async def dashboard_stats():

    db = SessionLocal()

    try:
        total_documents = db.query(VaultDocument).count()
        conversation_count = db.query(ConversationMemory).count()
        total_vectors = conversation_count * 12
        ai_requests = conversation_count
        active_tasks = 3

        return {
            "total_documents": total_documents,
            "total_vectors": total_vectors,
            "ai_requests": ai_requests,
            "active_tasks": active_tasks
        }

    finally:
        db.close()
    