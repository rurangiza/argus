from pydantic import BaseModel


class Message(BaseModel):
	role: str
	content: str


class ChatRequest(BaseModel):
	messages: list[Message]
