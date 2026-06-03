class QueryRouter:

    @staticmethod
    def detect_intent(question: str):

        q = question.lower()

        # =========================
        # GENERAL CHAT
        # =========================

        general_chat_words = [

            "hello",
            "hi",
            "hey",
            "how are you",
            "who are you",
            "good morning",
            "good evening"
        ]

        if any(word == q.strip() for word in general_chat_words):

            return "general_chat"

        # =========================
        # DOCUMENT STATS
        # =========================

        if any(word in q for word in [

            "how many documents",
            "document count",
            "files uploaded",
            "total files",
            "how much documents"
        ]):

            return "document_stats"

        # =========================
        # DOCUMENT QUESTIONS
        # =========================

        if any(word in q for word in [

            "document",
            "file",
            "uploaded",
            "pdf",
            "resume",
            "what does this contain",
            "summarize",
            "summary",
            "what is inside"
        ]):

            return "rag_query"

        # =========================
        # SECURITY ANALYSIS
        # =========================

        if any(word in q for word in [

            "security",
            "risk",
            "vulnerability",
            "attack",
            "threat"
        ]):

            return "security_analysis"

        # =========================
        # DEFAULT
        # =========================

        return "rag_query"