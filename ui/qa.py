from uuid import uuid4 as uuid

import httpx
import streamlit as st
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    message: str


def send_query(messages: list[Message], usableTools: list[str]):
    BASE_URL = 'http://127.0.0.1:8000'
    return httpx.post(
        f'{BASE_URL}/v1/chat/',
        json={
            'messages': messages,
            'tools': usableTools,
            'model': 'gpt-4o-mini',
            'temperature': 0.6,
            'stream': False,
            'top_p': 1,
        },
        timeout=15,
    )


if 'messages' not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant', 'content': 'How can I help you?'}
    ]

if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = uuid()

with st.sidebar:
    st.markdown('### Tools')
    tools = {
        'GetWeather': st.checkbox('Weather'),
        'datetime': st.checkbox('Datetime', disabled=True),
        'url-integration': st.checkbox('URL Integration', disabled=True),
    }
    if tools['GetWeather']:
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

    response: ChatResponse = send_query(
        st.session_state.messages,
        [name for name, isEnabled in tools.items() if isEnabled],
    )
    if response.is_error:
        st.write(response.json()['detail'])

    body = response.json()

    st.session_state.messages.append(
        {'role': 'assistant', 'content': body['message']}
    )
    with st.chat_message('assistant'):
        st.write(body['message'])
