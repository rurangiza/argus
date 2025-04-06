"""Router module for chat-related endpoints."""

from fastapi import APIRouter
from .models import ChatRequest


router = APIRouter(prefix='/chat')


@router.post('/')
async def invoke(request: ChatRequest):
	return {'message': f'You said: {request.messages[-1].content}'}


@router.get('/')
async def hello() -> dict[str, str]:
	"""Return a greeting message for the chat endpoint."""
	return {'message': 'How may I help you?'}
