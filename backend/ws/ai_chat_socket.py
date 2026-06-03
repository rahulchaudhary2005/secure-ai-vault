from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from ai.    RAGEngine
)


class AIChatSocket:

    active_connections = []

    @staticmethod
    async def connect(
        websocket: WebSocket
    ):

        await websocket.accept()

        AIChatSocket.active_connections.append(
            websocket
        )

    @staticmethod
    def disconnect(
        websocket: WebSocket
    ):

        AIChatSocket.active_connections.remove(
            websocket
        )

    @staticmethod
    async def handle_chat(
        websocket: WebSocket
    ):

        await AIChatSocket.connect(
            websocket
        )

        try:

            while True:

                data = await websocket.receive_json()

                question = data.get(
                    "question"
                )

                owner_email = data.get(
                    "owner_email"
                )

                response = (
                    RAGEngine.ask_question(

                        question=question,

                        owner_email=owner_email
                    )
                )

                await websocket.send_json({

                    "success": True,

                    "ai_response": (
                        response["answer"]
                    ),

                    "documents_found": (
                        response[
                            "documents_found"
                        ]
                    )
                })

        except WebSocketDisconnect:

            AIChatSocket.disconnect(
                websocket
            )