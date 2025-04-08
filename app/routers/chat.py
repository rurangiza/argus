"""Router module for chat-related endpoints."""

import json

from fastapi import APIRouter
from app.models import ChatRequest
from openai import OpenAI
from app.config import settings
from app.utils.tools import ToolsRegistry


router = APIRouter(prefix='/chat')
client = OpenAI(api_key=settings.openai_api_key)


@router.post('/')
async def invoke(request: ChatRequest):
	messages = request.messages
	available_tools, tools_descriptions = ToolsRegistry.filter(request.tools)

	completion = client.chat.completions.create(
		messages=messages,
		model='gpt-4o-mini',
		temperature=0.6,
		stream=False,
		top_p=1,
		tools=tools_descriptions,
	)
	if tool_calls := completion.choices[0].message.tool_calls:
		for idx, tool in enumerate(tool_calls):
			messages.append(completion.choices[0].message)

			chosen_function = tool.function.name
			args = json.loads(tool.function.arguments)

			result = available_tools[chosen_function]['function'](**args)

			messages.append(
				{'role': 'tool', 'tool_call_id': tool.id, 'content': str(result)}
			)

			completion = client.chat.completions.create(
				model='gpt-4o-mini',
				messages=messages,
				tools=tools_descriptions,
				temperature=0.6,
				stream=False,
				top_p=1,
			)
			if idx == len(tool_calls) - 1:
				return {'message': completion.choices[0].message.content}
	return {'message': completion.choices[0].message.content}


@router.get('/')
async def hello() -> dict[str, str]:
	"""Return a greeting message for the chat endpoint."""
	return {'message': 'How may I help you?'}
