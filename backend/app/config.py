from pydantic_settings import BaseSettings, SettingsConfigDict

class Configurations(BaseSettings):
  APP_NAME: str = "Clean Architecture Blogsite"
  DATABASE_URL: str = "sqlite:///./test.db"
  DEBUG: bool = True
  DB_ECHO: bool = False
  SECRET_KEY: str = "your_secret_key"
  ALGORITHM: str = "HS256"
  DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
  DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS: int = 1
  
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8"
  )

config = Configurations()