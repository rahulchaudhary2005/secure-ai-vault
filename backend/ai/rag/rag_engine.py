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

from ai.router.query_router import (
    QueryRouter
)


class RAGEngine:

    @staticmethod
    def ask_question(

        question: str,

        owner_email: str,

        filenames: list = None
    ):

        try:

            # =====================================
            # VALIDATE QUESTION
            # =====================================

            question = question.strip()

            if not question:

                return {

                    "success": False,

                    "error":
                        "Question cannot be empty."
                }

            # =====================================
            # DETECT INTENT
            # =====================================

            intent = (
                QueryRouter
                .detect_intent(
                    question
                )
            )

            # =====================================
            # FAST GENERAL CHAT
            # =====================================

            if intent == "general_chat":

                response = (

                    OllamaEngine
                    .generate_response(
                        question
                    )
                )

                return {

                    "success": True,

                    "intent": intent,

                    "enterprise_ai": True,

                    "answer": response
                }

            # =====================================
            # DOCUMENT STATS
            # =====================================

            if intent == "document_stats":

                stats = (

                    ChromaEngine
                    .get_collection_stats(
                        owner_email
                    )
                )

                return {

                    "success": True,

                    "intent": intent,

                    "enterprise_ai": True,

                    "answer": (

                        f"You currently have "

                        f"{stats['total_vectors']} "

                        f"document chunks stored "

                        f"in your secure AI database."
                    ),

                    "documents_found":
                        stats["total_vectors"]
                }

            # =====================================
            # GENERATE QUERY EMBEDDING
            # =====================================

            query_embedding = (

                EmbeddingService
                .generate_embedding(
                    question
                )
            )

            # =====================================
            # VECTOR SEARCH
            # =====================================

            documents = []

            if filenames:

                for fname in filenames:

                    print("\n========== FILE SEARCH ==========")
                    print("Searching File:", fname)
                    print("=================================\n")

                    results = (

                        ChromaEngine
                        .semantic_search(

                            owner_email=
                                owner_email,

                            query_embedding=
                                query_embedding,

                            limit=3,

                            metadata_filter={

                                "stored_filename": {

                                    "$eq": fname
                                }
                            }
                        )
                    )

                    # =====================================
                    # DEBUGGING
                    # =====================================

                    print(
                        "\n========== FILTER DEBUG =========="
                    )

                    print(
                        "Selected Filename:",
                        fname
                    )

                    print(
                        "Results:",
                        results
                    )

                    print(
                        "=================================\n"
                    )

                    docs = (
                        results.get(
                            "documents",
                            [[]]
                        )[0]
                    )

                    documents.extend(docs)

            else:

                results = (

                    ChromaEngine
                    .semantic_search(

                        owner_email=
                            owner_email,

                        query_embedding=
                            query_embedding,

                        limit=4
                    )
                )

                documents = (
                    results.get(
                        "documents",
                        [[]]
                    )[0]
                )

            # =====================================
            # REMOVE DUPLICATES
            # =====================================

            unique_documents = []

            seen = set()

            for doc in documents:

                if (

                    doc
                    and isinstance(doc, str)
                    and doc not in seen
                    and len(doc.strip()) > 20
                ):

                    seen.add(doc)

                    unique_documents.append(
                        doc.strip()
                    )

            # =====================================
            # NO DOCUMENTS FOUND
            # =====================================

            if not unique_documents:

                return {

                    "success": True,

                    "enterprise_ai": True,

                    "intent": intent,

                    "answer": (
                        "I could not find any "
                        "relevant information "
                        "inside the uploaded "
                        "documents."
                    ),

                    "documents_found": 0
                }

            # =====================================
            # CLEAN CONTEXT
            # =====================================

            cleaned_docs = []

            for doc in unique_documents:

                # REMOVE OCR NOISE

                if any(

                    noise in doc.lower()

                    for noise in [

                        "dashboard",
                        "view all",
                        "mock interview",
                        "agent logs",
                        "question generator",
                        "recent activity",
                        "premium plan",
                        "days ago"
                    ]
                ):

                    continue

                cleaned_docs.append(doc)

            # =====================================
            # FALLBACK
            # =====================================

            if not cleaned_docs:

                cleaned_docs = unique_documents[:2]

            # =====================================
            # LIMIT CONTEXT
            # =====================================

            retrieved_context = (

                "\n\n".join(
                    cleaned_docs[:3]
                )
            )

            retrieved_context = (
                retrieved_context[:3000]
            )

            # =====================================
            # MEMORY CONTEXT
            # =====================================

            memory_context = (

                ContextBuilder
                .build_context(
                    owner_email
                )
            )

            memory_context = (
                memory_context[:300]
            )

            # =====================================
            # GENERATE AI RESPONSE
            # =====================================

            ai_response = (

                OllamaEngine
                .generate_rag_response(

                    question=
                        question,

                    retrieved_context=
                        retrieved_context
                )
            )

            # =====================================
            # FALLBACK RESPONSE
            # =====================================

            if (

                not ai_response
                or len(ai_response.strip()) < 5
            ):

                ai_response = (

                    "Unable to generate "
                    "AI response."
                )

            # =====================================
            # SAVE MEMORY
            # =====================================

            try:

                if len(question) < 300:

                    ConversationMemoryEngine.save_memory(

                        owner_email=
                            owner_email,

                        user_message=
                            question,

                        ai_response=
                            ai_response[:500],

                        semantic_tag=
                            intent
                    )

            except Exception as memory_error:

                print(
                    "Memory Save Error:",
                    memory_error
                )

            # =====================================
            # FINAL RESPONSE
            # =====================================

            return {

                "success": True,

                "enterprise_ai": True,

                "intent": intent,

                "question": question,

                "answer": ai_response,

                "documents_found":
                    len(cleaned_docs),

                "semantic_search_enabled":
                    True,

                "conversation_memory_enabled":
                    True,

                "secure_rag_enabled":
                    True
            }

        except Exception as e:

            print(
                "RAG ENGINE ERROR:",
                str(e)
            )

            return {

                "success": False,

                "enterprise_rag_error":
                    True,

                "error": str(e)
            }