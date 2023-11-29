from fastapi import APIRouter

from .endpoints import movie

v1_router = APIRouter()
v1_router.include_router(
    movie.router,
    prefix="/movie",
    tags=["movie"],
)
