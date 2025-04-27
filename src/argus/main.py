from fastapi import FastAPI

from .api.v1 import router

app = FastAPI()
app.include_router(router)


@app.get('/health')
async def check_health() -> dict[str, str]:
    """Liveness check"""
    return {'health': 'ok'}


@app.get('/ready')
async def check_readiness() -> dict[str, str]:
    """Readiness check"""
    return {'status': 'ready'}
