from langchain_community.llms import Ollama

class OllamaEngine:

    llm = Ollama(
        model="phi3"
    )

    @staticmethod
    def generate_response(prompt: str):

        response = (
            OllamaEngine
            .llm
            .invoke(prompt)
        )

        return response