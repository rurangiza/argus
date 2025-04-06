"""Router module for chat-related endpoints."""

from fastapi import APIRouter
from app.models import Note


router = APIRouter(prefix='/notes')


@router.post('/')
async def add_note(note: Note):
	"""save notes to knowledge graph"""
	pass
