# Imports
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.schemas import ChatRequest, ChatResponse
from backend.services import ChatService


# Lifespan (startup / shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    app.state.model = None
    app.state.chat_service = ChatService()

    yield

    # Shutdown logic
    app.state.model = None
    app.state.chat_service = None


# Application instance
app = FastAPI(
    title="Airi API",
    description="Backend for Airi AI Companion",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Airi API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/history")
async def history_check():
    return [
        {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "messages": history,
        }
        for (user_id, conversation_id), history
        in app.state.chat_service.conversations.items()
    ]


@app.post("/chat", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    answer = app.state.chat_service.process_message(
        request.user_id, 
        request.conversation_id, 
        request.message
    )

    return ChatResponse(
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        response=answer
    )

app.mount(
    "/ui",
    StaticFiles(
        directory=Path(__file__).resolve().parent.parent / "frontend",
        html=True,
    ),
    name="frontend",
)