from fastapi import APIRouter
from app.api.endpoints import system, user, channel


api_router = APIRouter()
api_router.include_router(system.router, tags=['system'])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(channel.router, prefix="/channel", tags=["channel"])