"""Router module for chat-related endpoints."""

from fastapi import APIRouter

router = APIRouter(prefix="/chat")

@router.get("/")
async def invoke() -> dict[str, str]:
    """Return a greeting message for the chat endpoint."""
    return {"message": "How may I help you?"}
