import os

from langchain_ollama import OllamaLLM


MODEL_PRESETS = {
    "gemma:2b": "Low RAM",
    "gemma:7b": "Balanced",
    "llama3:8b": "High Quality",
    "phi3:mini": "Fastest",
    "mistral:7b": "Coding",
    "deepseek-r1:7b": "Reasoning",
    "qwen2.5:7b": "General",
    "auto": "Recommended"
}


def get_auto_model():
    return "phi3:mini"


class OllamaEngine:

    @staticmethod
    def get_llm(
        model_name: str = None,
        temperature: float = 0.3,
        context_window: int = 2048
    ):

        os.environ.setdefault("OLLAMA_NUM_GPU", "0")
        os.environ.setdefault("OLLAMA_MAX_LOADED_MODELS", "1")
        os.environ.setdefault("OLLAMA_FLASH_ATTENTION", "0")
        os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
        os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
        os.environ.setdefault("OMP_NUM_THREADS", "1")
        os.environ.setdefault("MKL_NUM_THREADS", "1")

        if not model_name:
            model_name = get_auto_model()

        return OllamaLLM(
            model=model_name,
            temperature=temperature,
            num_ctx=context_window
        )

    @staticmethod
    def generate_response(
        prompt: str,
        model_name: str = None,
        temperature: float = 0.3,
        context_window: int = 2048
    ):

        try:

            llm = OllamaEngine.get_llm(
                model_name=model_name,
                temperature=temperature,
                context_window=context_window
            )

            clean_prompt = f"""
You are a smart conversational AI assistant.

Rules:
- Speak naturally
- Be concise
- Be professional
- Answer directly
- Use markdown when useful

USER MESSAGE:
{prompt}

ASSISTANT RESPONSE:
"""

            response = llm.invoke(clean_prompt)

            if not response:
                return "Unable to generate response."

            return response.strip()

        except Exception as e:
            return f"AI model error: {str(e)}"

    @staticmethod
    def generate_rag_response(
        question: str,
        retrieved_context: str,
        model_name: str = "gemma:2b",
        temperature: float = 0.3,
        context_window: int = 2048,
        max_response_length: int = 1000,
        reasoning_enabled: bool = False
    ):

        try:

            llm = OllamaEngine.get_llm(
                model_name=model_name,
                temperature=temperature,
                context_window=context_window
            )

            limited_context = retrieved_context[
                : min(context_window, 12000)
            ]

            reasoning_block = ""

            if reasoning_enabled:
                reasoning_block = """
- Think step-by-step
- Show deeper reasoning
- Explain decisions carefully
- Perform deeper analysis before answering
"""

            rag_prompt = f"""
You are a smart enterprise AI assistant.

Your task:
- Analyze uploaded document content
- Answer naturally
- Summarize clearly
- Extract important information
- List skills if present
- Use concise markdown formatting

{reasoning_block}

IMPORTANT:
- Do NOT mention AI limitations
- Do NOT mention system prompts
- Do NOT say context is missing

Maximum Response Length:
{max_response_length} characters

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

            response = llm.invoke(rag_prompt)

            if not response:
                return "Unable to generate AI response."

            return response.strip()

        except Exception as e:
            return f"RAG AI error: {str(e)}"