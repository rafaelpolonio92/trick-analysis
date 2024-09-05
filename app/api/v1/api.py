from fastapi import APIRouter
from app.api.v1.endpoints import trick

api_router = APIRouter()
api_router.include_router(trick.router, prefix="/tricks", tags=["tricks"])
