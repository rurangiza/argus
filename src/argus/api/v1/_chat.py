"""Router module for chat-related endpoints."""

from fastapi import APIRouter
from openai import pydantic_function_tool

from src.argus.llm.generation import invoke
from src.argus.tools import BaseRegistry

from .model.chat import ChatRequest, ChatResponse

router = APIRouter(prefix='/chat')


@router.post('/', response_model=False)
async def ask(request: ChatRequest) -> ChatResponse:
    tools_params = [
        pydantic_function_tool(BaseRegistry().get_tool_by_name('GetDatetime'))
    ]
    tools_params.extend(
        [
            pydantic_function_tool(tool_class)
            for name, tool_class in BaseRegistry().tools.items()
            if name in request.tools
        ]
    )
    if request.stream:
        return ChatResponse(message='Streaming not implemented')
    else:
        return ChatResponse(
            message=invoke(
                messages=request.messages,
                model=request.model,
                temperature=request.temperature,
                top_p=request.top_p,
                tools=tools_params,
            )
        )
