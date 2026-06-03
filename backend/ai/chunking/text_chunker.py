from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class TextChunker:

    @staticmethod
    def chunk_text(text: str):

        splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=300,

                chunk_overlap=40
            )
        )

        chunks = splitter.split_text(text)

        clean_chunks = []

        blocked_words = [

            "dashboard",
            "view all",
            "search anything",
            "activity",
            "progress tracker",
            "interview plan",
            "mock interview",
            "question bank",
            "feedback",
            "skill gap",
            "voice interview"
        ]

        for chunk in chunks:

            chunk = chunk.strip()

            if len(chunk) < 80:
                continue

            lower_chunk = chunk.lower()

            skip = False

            for word in blocked_words:

                if word in lower_chunk:

                    skip = True
                    break

            if not skip:

                clean_chunks.append(chunk)

        return clean_chunks