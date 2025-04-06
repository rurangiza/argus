import streamlit as st
import httpx
from uuid import uuid4 as uuid
from pydantic import BaseModel


class Message(BaseModel):
	role: str
	content: str


class ChatResponse(BaseModel):
	message: str


def send_query(messages: list[Message]):
	BASE_URL = 'http://127.0.0.1:8000'
	r = httpx.post(
		f'{BASE_URL}/chat/',
		json={
			'messages': messages,
		},
	)
	return r.json()


if 'messages' not in st.session_state:
	st.session_state.messages = []

if 'conversation_id' not in st.session_state:
	st.session_state.conversation_id = uuid()


st.markdown('# Argus')
st.markdown('### A conversational tool for your personal knowledge')

for message in st.session_state.messages:
	with st.chat_message(message['role']):
		st.markdown(message['content'])

if prompt := st.chat_input('Ask anything'):
	st.session_state.messages.append({'role': 'user', 'content': prompt})
	with st.chat_message('user'):
		st.markdown(prompt)

	answer: ChatResponse = send_query(st.session_state.messages)
	st.session_state.messages.append(
		{'role': 'assistant', 'content': answer['message']}
	)
	with st.chat_message('assistant'):
		st.markdown(answer['message'])
