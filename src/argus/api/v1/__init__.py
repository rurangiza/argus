from fastapi import APIRouter

from ._chat import router as chat

router: APIRouter = APIRouter(prefix='/v1', tags=['v1'])
router.include_router(chat)

__all__ = ['router']
