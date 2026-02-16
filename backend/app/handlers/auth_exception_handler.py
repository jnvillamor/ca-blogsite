import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from jwt import PyJWTError, ExpiredSignatureError, InvalidTokenError, DecodeError

from app.auth.auth_exceptions import AuthException

default_logger = logging.getLogger("uvicorn.error")

def register_auth_exception_handler(
  app: FastAPI, 
  logger: logging.Logger = default_logger
):
  @app.exception_handler(InvalidTokenError)
  def handle_invalid_token_exception(
    request: Request, 
    exc: InvalidTokenError
  ):
    logger.error(f"InvalidTokenError: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_401_UNAUTHORIZED,
      content={"detail": "Invalid token"}
    )
  
  @app.exception_handler(ExpiredSignatureError)
  def handle_expired_signature_exception(
    request: Request,
    exc: ExpiredSignatureError
  ):
    logger.error(f"ExpiredSignatureError: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_401_UNAUTHORIZED,
      content={"detail": "Token has expired"}
    )
  
  @app.exception_handler(DecodeError)
  def handle_decode_error_exception(
    request: Request,
    exc: DecodeError
  ):
    logger.error(f"DecodeError: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_401_UNAUTHORIZED,
      content={"detail": "Failed to decode token"}
    )
  
  @app.exception_handler(PyJWTError)
  def handle_pyjwt_error_exception(
    request: Request,
    exc: PyJWTError
  ):
    logger.error(f"PyJWTError: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_401_UNAUTHORIZED,
      content={"detail": "Token verification failed"}
    )
  
  @app.exception_handler(AuthException)
  def handle_auth_exception(
    request: Request,
    exc: AuthException
  ):
    logger.error(f"AuthException: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_401_UNAUTHORIZED,
      content={"detail": str(exc)}
    )
