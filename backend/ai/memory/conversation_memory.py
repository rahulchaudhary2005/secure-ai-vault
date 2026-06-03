from database.database import (
    SessionLocal
)

from database.models import (
    ConversationMemory
)


class ConversationMemoryEngine:

    @staticmethod
    def save_memory(

        owner_email: str,

        user_message: str,

        ai_response: str,

        semantic_tag: str = "general"

    ):

        db = SessionLocal()

        try:

            memory = ConversationMemory(

                owner_email=owner_email,

                user_message=user_message,

                ai_response=ai_response,

                semantic_tag=semantic_tag
            )

            db.add(memory)

            db.commit()

            db.refresh(memory)

            return memory

        finally:

            db.close()

    @staticmethod
    def get_recent_memories(

        owner_email: str,

        limit: int = 5

    ):

        db = SessionLocal()

        try:

            memories = (

                db.query(
                    ConversationMemory
                )

                .filter(
                    ConversationMemory.owner_email
                    == owner_email
                )

                .order_by(
                    ConversationMemory.id.desc()
                )

                .limit(limit)

                .all()
            )

            return memories

        finally:

            db.close()