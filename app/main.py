"""Main application module for the FastAPI application."""

from fastapi import FastAPI
from .routers import chat


app = FastAPI()
app.include_router(chat.router)


@app.get('/')
async def hello() -> dict[str, str]:
	"""Return a simple hello world message."""
	return {'message': 'Hello, world'}
