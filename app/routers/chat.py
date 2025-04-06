"""Router module for chat-related endpoints."""

from fastapi import APIRouter
from app.models import ChatRequest
from openai import OpenAI
from app.config import settings


router = APIRouter(prefix='/chat')
client = OpenAI(api_key=settings.openai_api_key)


@router.post('/')
async def invoke(request: ChatRequest):
	messages = request.messages
	completion = client.chat.completions.create(
			messages=messages,
			model="gpt-4o-mini",
			temperature=0.6,
			top_p=1,
	)
	return {
		"message": completion.choices[0].message.content
	}


@router.get('/')
async def hello() -> dict[str, str]:
	"""Return a greeting message for the chat endpoint."""
	return {'message': 'How may I help you?'}
