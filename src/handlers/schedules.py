from enum import Enum

from fastapi import APIRouter, status

from src.models.schedule import Schedule, Semesters, Campuses
from src.settings import settings
from src.utils.rutgers import RutgersScheduleOfClasses

router = APIRouter()

app_settings = settings.get_settings()


@router.get(
    path="/schedules",
    status_code=status.HTTP_200_OK,
    tags=["Schedule Generator"],
    response_model=Schedule,
)
async def retrieve_schedules(year: str, term: Semesters, campus: Campuses):
    """Retrieves schedule of classes from Rutgers University's Schedule of Classes API"""
    schedule = RutgersScheduleOfClasses(year=year, term=term, campus=campus)

    classes = schedule.fetch_filtered_schedule_of_classes()

    return dict(response=classes)


@router.get(path="/health", status_code=status.HTTP_200_OK)
async def health_check_status():
    return {"status": "ok"}
