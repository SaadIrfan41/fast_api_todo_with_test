from fastapi import APIRouter

from api.router import login,todo,user

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"],responses={404: {"description": "Route Not found"}})
api_router.include_router(todo.router, tags=["Todos"],responses={404: {"description": "Route Not found"}})
api_router.include_router(user.router, tags=["Users"],responses={404: {"description": "Route Not found"}})