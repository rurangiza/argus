import json

from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam

from src.argus.api.v1.model.chat import ChatMessage
from src.argus.config import settings
from src.argus.exception import ToolNotFound
from src.argus.tools import BaseRegistry

client = OpenAI(api_key=settings.openai_api_key)


def invoke(
    messages: list[ChatMessage],
    model: str = 'gpt-4o-mini',
    temperature: float = 0.7,
    top_p: float = 1.0,
    tools: list[ChatCompletionToolParam] = [],
) -> str:
    registry = BaseRegistry()

    completion = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        stream=False,
        top_p=top_p,
        tools=tools,
    )

    messages.append(completion.choices[0].message)
    if tool_calls := completion.choices[0].message.tool_calls:
        for idx, tool_call in enumerate(tool_calls):
            try:
                ChosenTool = registry.get_tool_by_name(tool_call.function.name)
                args = json.loads(tool_call.function.arguments)

                messages.append(
                    {
                        'role': 'tool',
                        'tool_call_id': tool_call.id,
                        'content': ChosenTool(**args).resolve(),
                    }
                )
            except ToolNotFound:
                messages.append(
                    {
                        'role': 'assistant',
                        'tool_call_id': tool_call.id,
                        'content': 'None',
                    }
                )
            tc_completion = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=messages,
                temperature=0.6,
                stream=False,
                top_p=1,
                tools=tools,
                tool_choice='none',
            )
            messages.append(tc_completion.choices[0].message)
    return messages[-1].content


def stream():
    pass
