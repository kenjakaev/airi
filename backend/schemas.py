from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    conversation_id: str
    message: str


class ChatResponse(BaseModel):
    user_id: str
    conversation_id: str
    response: str