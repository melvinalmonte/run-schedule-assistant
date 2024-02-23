from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from src.api import router

app_settings = settings.get_settings()


def create_app():

    app = FastAPI(
        title=app_settings.APP_TITLE,
        description=app_settings.APP_DESCRIPTION,
        version=app_settings.APP_VERSION,
        docs_url=app_settings.APP_DOCS_URL,
        openapi_url=app_settings.APP_OPENAPI_URL,
    )

    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get(path="/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/api/docs")

    return app
