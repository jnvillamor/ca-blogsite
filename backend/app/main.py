import logging
import app.logger
from fastapi import FastAPI
from app.config import config
from app.api.v1 import register_routes
from app.handlers import register_handlers

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
  app = FastAPI(title=config.APP_NAME)

  @app.get("/")
  async def health_check():
    return {"status": "ok"}
  
  register_routes(app)
  register_handlers(app, logger=logger)

  return app

app = create_app()