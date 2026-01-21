from fastapi import FastAPI
from app.config import config
from app.api.v1 import register_routes

def create_app() -> FastAPI:
  app = FastAPI(title=config.APP_NAME)

  @app.get("/")
  async def health_check():
    return {"status": "ok"}
  
  register_routes(app)

  return app

app = create_app()