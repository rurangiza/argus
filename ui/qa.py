import streamlit as st
import httpx
from uuid import uuid4 as uuid
from pydantic import BaseModel


class Message(BaseModel):
	role: str
	content: str


class ChatResponse(BaseModel):
	message: str


def send_query(messages: list[Message], usableTools: list[str]):
	BASE_URL = 'http://127.0.0.1:8000'
	r = httpx.post(
		f'{BASE_URL}/chat/',
		json={
			'messages': messages,
			'tools': usableTools,
		},
	)
	return r.json()


if 'messages' not in st.session_state:
	st.session_state.messages = [
		{'role': 'assistant', 'content': 'How can I help you?'}
	]

if 'conversation_id' not in st.session_state:
	st.session_state.conversation_id = uuid()

with st.sidebar:
	st.markdown('### Tools')
	tools = {
		'get_weather': st.checkbox('Weather'),
		'datetime': st.checkbox('Datetime', disabled=True),
		'url-integration': st.checkbox('URL Integration', disabled=True),
	}
	if tools['get_weather']:
		st.write(
			"You can now get the weather of any city. `Example: what's the weather in Paris?`"
		)

st.markdown('# Q&A')

for message in st.session_state.messages:
	with st.chat_message(message['role']):
		st.markdown(message['content'])

if prompt := st.chat_input('Ask anything'):
	st.session_state.messages.append({'role': 'user', 'content': prompt})
	with st.chat_message('user'):
		st.markdown(prompt)

	answer: ChatResponse = send_query(
		st.session_state.messages,
		[name for name, isEnabled in tools.items() if isEnabled],
	)
	st.session_state.messages.append(
		{'role': 'assistant', 'content': answer['message']}
	)
	with st.chat_message('assistant'):
		st.write(answer['message'])
