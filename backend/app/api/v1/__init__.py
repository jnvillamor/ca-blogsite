from fastapi import FastAPI

def register_routes(app: FastAPI):
  from .auth_endpoint import router as auth_router
  app.include_router(prefix="/v1", router=auth_router)

  from .blog_endpoint import router as blog_router
  app.include_router(prefix="/v1", router=blog_router)

  from .user_endpoint import router as user_router
  app.include_router(prefix="/v1", router=user_router)
