from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .domain_exception_handler import register_domain_exception_handler 
from .auth_exception_handler import register_auth_exception_handler
import logging

logger = logging.getLogger(__name__)

def register_handlers(app: FastAPI, logger: logging.Logger = logger):
  @app.exception_handler(Exception)
  def handle_generic_exception(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      content={"detail": "An unexpected error occurred."}
    )
  
  @app.exception_handler(RequestValidationError)
  def handle_validation_exception(request: Request, exc: RequestValidationError):
    logger.error(f"Request validation error: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
      content={
        "message": "Invalid request data",
        "details": exc.errors()
      }
    )
  
  register_auth_exception_handler(app, logger=logger)
  register_domain_exception_handler(app, logger=logger)