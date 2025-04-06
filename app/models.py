from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
	role: str
	content: str


class ChatRequest(BaseModel):
	messages: list[Message]


class Note(BaseModel):
	date: datetime
	content: str
	location: str


class ToolParameterProperty(BaseModel):
	description: str
	type: str


class ToolDescription(BaseModel):
	description: str
	properties: dict[str, ToolParameterProperty] | None
