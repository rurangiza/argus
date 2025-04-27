from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    tools: list[str]
    temperature: float
    top_p: float
    model: str
    stream: bool


class ChatResponse(BaseModel):
    message: str


class ToolParameterProperty(BaseModel):
    description: str
    type: str


class ToolDescription(BaseModel):
    description: str
    properties: dict[str, ToolParameterProperty] | None
