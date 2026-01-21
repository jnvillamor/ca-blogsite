from fastapi import FastAPI

def register_routes(app: FastAPI):
  from .user_endpoint import router as user_router
  app.include_router(user_router)