from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .domain import register_exception_handler
import logging

def register_handlers(app: FastAPI, logger: logging.Logger = None):
  @app.exception_handler(Exception)
  def handle_generic_exception(request: Request, exc: Exception):
    return JSONResponse(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      content={"detail": "An unexpected error occurred."}
    )

  register_exception_handler(app, logger=logger)