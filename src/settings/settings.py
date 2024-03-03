from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application Information
    APP_TITLE: str = "Rutgers Schedule of Classes API"
    APP_DESCRIPTION: str = "Simple API to get schedule of classes from Rutgers University"
    APP_VERSION: str = "0.1.0"

    # API Endpoints
    APP_DOCS_URL: str = "/api/docs"
    APP_OPENAPI_URL: str = "/api/openapi.json"

    # Server Configuration
    PORT: int = 8000
    ALLOWED_HOSTS: List[str] = ["*"]

    # User Roles
    READER_ROLE: str
    BUCKET_NAME: str

    # Redis Configuration
    REDISHOST: str = "localhost"
    REDISPASSWORD: str = "admin"
    REDISPORT: int = 6379


@lru_cache()
def get_settings():
    settings = Settings()
    return settings
