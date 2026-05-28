from ai.embeddings.embedding_service import (
    EmbeddingService
)

from ai.vector_db.chroma_engine import (
    ChromaEngine
)

from ai.langchain.ollama_engine import (
    OllamaEngine
)

from ai.memory.context_builder import (
    ContextBuilder
)

from ai.memory.conversation_memory import (
    ConversationMemoryEngine
)


class RAGEngine:

    @staticmethod
    def ask_question(

        question: str,

        owner_email: str,
        filenames: list = None

    ):

        try:

            # ===================================
            # VALIDATE QUESTION
            # ===================================

            if not question.strip():

                return {

                    "success": False,

                    "error":
                        "Question cannot be empty"
                }

            # ===================================
            # GENERATE QUERY EMBEDDING
            # ===================================

            query_embedding = (

                EmbeddingService
                .generate_embedding(
                    question
                )
            )

            # ===================================
            # ENTERPRISE VECTOR SEARCH
            # ===================================

            documents = []

            if filenames:

                # search by each specified source filename and collect results
                for fname in filenames:

                    results = ChromaEngine.semantic_search(

                        owner_email=owner_email,

                        query_embedding=query_embedding,

                        limit=5,

                        metadata_filter={"source_filename": fname}
                    )

                    docs = results.get("documents", [[]])[0]

                    documents.extend(docs)

            else:

                results = ChromaEngine.semantic_search(

                    owner_email=owner_email,

                    query_embedding=query_embedding,

                    limit=5
                )

                documents = results.get("documents", [[]])[0]

            # ===================================
            # SAFE DOCUMENT FALLBACK
            # ===================================

            if not documents:

                retrieved_context = (
                    "No relevant secure vault "
                    "documents found."
                )

            else:

                retrieved_context = (
                    "\n".join(documents)
                )

            # ===================================
            # MEMORY CONTEXT
            # ===================================

            memory_context = (

                ContextBuilder
                .build_context(
                    owner_email
                )
            )

            # ===================================
            # SAFE MEMORY FALLBACK
            # ===================================

            if not memory_context:

                memory_context = (
                    "No previous conversation memory."
                )

            # ===================================
            # ENTERPRISE AI PROMPT
            # ===================================

            full_prompt = f'''

You are an advanced enterprise AI cybersecurity assistant.

You must answer ONLY from:
1. Retrieved enterprise vault data
2. Previous AI memory
3. Secure semantic context

Do NOT hallucinate.
Do NOT invent information.
If information is unavailable,
say clearly that it was not found.

===============================
PREVIOUS CONVERSATION MEMORY
===============================

{memory_context}

===============================
RETRIEVED AI KNOWLEDGE
===============================

{retrieved_context}

===============================
USER QUESTION
===============================

{question}

===============================
AI RESPONSE
===============================

'''

            # ===================================
            # OLLAMA RESPONSE
            # ===================================

            ai_response = (

                OllamaEngine
                .generate_response(
                    full_prompt
                )
            )

            # ===================================
            # SAFE AI RESPONSE FALLBACK
            # ===================================

            if not ai_response:

                ai_response = (

                    "Unable to generate "
                    "AI response."
                )

            # ===================================
            # SAVE MEMORY
            # ===================================

            ConversationMemoryEngine.save_memory(

                owner_email=owner_email,

                user_message=question,

                ai_response=ai_response,

                semantic_tag="rag_chat"
            )

            # ===================================
            # ENTERPRISE RESPONSE
            # ===================================

            return {

                "success": True,

                "enterprise_ai": True,

                "question": question,

                "answer": ai_response,

                "retrieved_context":
                    retrieved_context,

                "memory_context":
                    memory_context,

                "documents_found":
                    len(documents),

                "semantic_search_enabled":
                    True,

                "conversation_memory_enabled":
                    True,

                "secure_rag_enabled":
                    True
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e),

                "enterprise_rag_error": True
            }