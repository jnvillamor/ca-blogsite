from fastapi import FastAPI
from config import config

def create_app() -> FastAPI:
  app = FastAPI(title=config.APP_NAME)

  @app.get("/")
  async def health_check():
    return {"status": "ok"}
  
  return app

app = create_app()