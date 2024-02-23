from fastapi import APIRouter

from src.handlers import schedules

router = APIRouter(prefix="/api")

router.include_router(schedules.router, tags=["Schedule Generator"])
