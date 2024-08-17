import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    DEBUG: bool = False
    API_VERSION: str = os.environ.get("API_VERSION")
    ALGORITHM: str = os.environ.get("ALGORITHM")


settings = Settings()
