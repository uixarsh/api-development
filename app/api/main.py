from fastapi import APIRouter

from app.api.routes import login, post, user, vote

api_router = APIRouter()
api_router.include_router(post.router)
api_router.include_router(user.router)
api_router.include_router(login.router)
api_router.include_router(vote.router)