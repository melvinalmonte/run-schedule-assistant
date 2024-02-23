from src.app import create_app
from src.settings import settings
from src.api import router

app_settings = settings.get_settings()

app = create_app()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=app_settings.PORT, reload=True)
