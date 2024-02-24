from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Rutgers Schedule of Classes API"
    APP_DESCRIPTION: str = "Simple API to get schedule of classes from Rutgers University"
    APP_VERSION: str = "0.1.0"
    APP_DOCS_URL: str = "/api/docs"
    APP_OPENAPI_URL: str = "/api/openapi.json"
    PORT: int = 8000
    ALLOWED_HOSTS: List[str] = ["*"]


@lru_cache()
def get_settings():
    settings = Settings()
    return settings
