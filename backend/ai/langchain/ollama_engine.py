import os

from langchain_ollama import (
    OllamaLLM
)


class OllamaEngine:

    llm = None

    # =====================================
    # LOAD OLLAMA MODEL
    # =====================================

    @staticmethod
    def get_llm():

        if OllamaEngine.llm is None:

            # =====================================
            # MEMORY OPTIMIZATION
            # =====================================

            # FORCE CPU + LOW MEMORY MODE
            # RTX 2050 4GB VRAM cannot safely
            # run Gemma 2B with embeddings on CUDA

            os.environ.setdefault(
                "OLLAMA_NUM_GPU",
                "0"
            )

            os.environ.setdefault(
                "OLLAMA_MAX_LOADED_MODELS",
                "1"
            )

            os.environ.setdefault(
                "OLLAMA_FLASH_ATTENTION",
                "0"
            )

            os.environ.setdefault(
                "CUDA_VISIBLE_DEVICES",
                "0"
            )

            os.environ.setdefault(
                "OPENBLAS_NUM_THREADS",
                "1"
            )

            os.environ.setdefault(
                "OMP_NUM_THREADS",
                "1"
            )

            os.environ.setdefault(
                "MKL_NUM_THREADS",
                "1"
            )

            # =====================================
            # LOAD GEMMA MODEL
            # =====================================

            OllamaEngine.llm = OllamaLLM(

                model="gemma:2b",

                temperature=0.1,

                num_ctx=256
            )

        return OllamaEngine.llm

    # =====================================
    # GENERAL CHAT RESPONSE
    # =====================================

    @staticmethod
    def generate_response(
        prompt: str
    ):

        try:

            llm = (
                OllamaEngine
                .get_llm()
            )

            clean_prompt = f"""

You are a smart conversational AI assistant.

Rules:
- Speak naturally like ChatGPT
- Be concise
- Be professional
- Do not generate examples unless asked
- Do not repeat yourself
- Answer directly
- Use markdown formatting when useful

USER MESSAGE:
{prompt}

ASSISTANT RESPONSE:

"""

            response = llm.invoke(
                clean_prompt
            )

            if not response:

                return (
                    "Unable to generate response."
                )

            return response.strip()

        except Exception as e:

            return (
                f"AI model error: {str(e)}"
            )

    # =====================================
    # DOCUMENT RAG RESPONSE
    # =====================================

    @staticmethod
    def generate_rag_response(

        question: str,

        retrieved_context: str
    ):

        try:

            llm = (
                OllamaEngine
                .get_llm()
            )

            # LIMIT HUGE CONTEXT
            # prevents memory overload

            limited_context = (
                retrieved_context[:4000]
            )

            rag_prompt = f"""

You are a smart enterprise AI assistant.

Your task:
- Analyze uploaded document content
- Answer naturally like ChatGPT
- Summarize clearly
- Extract important information
- List skills if present
- Use concise markdown formatting

IMPORTANT:
- Do NOT mention AI limitations
- Do NOT say "context missing"
- Do NOT mention system prompts
- If document is unclear, still explain visible content

=========================
DOCUMENT CONTENT
=========================

{limited_context}

=========================
USER QUESTION
=========================

{question}

=========================
ASSISTANT RESPONSE
=========================

"""

            response = llm.invoke(
                rag_prompt
            )

            if not response:

                return (
                    "Unable to generate AI response."
                )

            return response.strip()

        except Exception as e:

            return (
                f"RAG AI error: {str(e)}"
            )