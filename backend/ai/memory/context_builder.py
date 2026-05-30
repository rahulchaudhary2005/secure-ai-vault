from backend.ai.memory.conversation_memory import (
    ConversationMemoryEngine
)


class ContextBuilder:

    @staticmethod
    def build_context(

        owner_email: str
    ):

        memories = (

            ConversationMemoryEngine
            .get_recent_memories(
                owner_email
            )
        )

        context = ""

        for memory in memories:

            context += f"""

User:
{memory.user_message}

AI:
{memory.ai_response}

"""

        return context