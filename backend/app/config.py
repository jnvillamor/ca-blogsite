from pydantic_settings import BaseSettings, SettingsConfigDict

class Configurations(BaseSettings):
  APP_NAME: str = "Clean Architecture Blogsite"
  DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
  DEBUG: bool = True
  DB_ECHO: bool = False
  
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8"
  )

config = Configurations()