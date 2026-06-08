from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket

from database.database import engine
from database.models import Base

# ============================================
# ROUTES
# ============================================

from api.routes.chat_routes import (
    router as chat_router
)

from api.routes.search_routes import (
    router as search_router
)

from api.routes.assistant_routes import (
    router as assistant_router
)

from api.routes.security_routes import (
    router as security_router
)

from api.routes.decrypt_routes import (
    router as decrypt_router
)

from api.routes.auth_routes import (
    router as auth_router
)

from api.routes.verify_routes import (
    router as verify_router
)

from api.routes.login_routes import (
    router as login_router
)

from api.routes.protected_routes import (
    router as protected_router
)

from api.routes.vault_routes import (
    router as vault_router
)

from api.routes.dashboard_routes import (
    router as dashboard_router
)

from api.routes.upload_routes import (
    router as upload_router
)

from api.routes.secure_file_sharing_routes import (
    router as secure_sharing_router
)

from api.routes.settings_routes import (
    router as settings_router
)

# ============================================
# DATABASE INIT
# ============================================

Base.metadata.create_all(bind=engine)

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="AI Secure Intelligence Vault",
    version="1.0.0",
    description="Offline AI Security Platform"
)

# ============================================
# CORS
# ============================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",

#         "https://secure-ai-vault-811g0e9g5-rahulchaudhary2005s-projects.vercel.app",

#         "https://secure-ai-vault-lndol.vercel.app"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# INCLUDE ROUTERS
# ============================================

app.include_router(upload_router)

app.include_router(chat_router)

app.include_router(search_router)

app.include_router(assistant_router)

app.include_router(security_router)

app.include_router(decrypt_router)

app.include_router(auth_router)

app.include_router(verify_router)

app.include_router(login_router)

app.include_router(protected_router)

app.include_router(vault_router)

app.include_router(dashboard_router)

app.include_router(secure_sharing_router)

app.include_router( settings_router)

# ============================================
# ROOT
# ============================================

@app.get("/")
async def root():

    return {

        "success": True,

        "message":
            "AI Secure Intelligence Vault Backend Running"
    }

# ============================================
# OPTIONAL WEBSOCKET
# ============================================

# from ws.ai_chat_socket import (
#     AIChatSocket
# )

# @app.websocket("/ws/ai-chat")
# async def websocket_chat(
#     websocket: WebSocket
# ):
#
#     await AIChatSocket.handle_chat(
#         websocket
#     )
