from enum import Enum

from fastapi import APIRouter, status

from src.utils.rutgers import RutgersScheduleOfClasses
from pydantic import BaseModel
from typing import List

router = APIRouter()


class Meeting(BaseModel):
    day: str
    time: str
    location: str


class Section(BaseModel):
    section: str
    instructor: str
    status: str
    meetings: List[str]


class CourseInfo(BaseModel):
    title: str
    courseCode: str
    credits: str
    sections: List[Section]


class Schedule(BaseModel):
    response: List[CourseInfo]


class Semesters(str, Enum):
    spring = "Spring"
    summer = "Summer"
    fall = "Fall"
    winter = "Winter"


class Campuses(str, Enum):
    newark = "Newark"
    new_brunswick = "New Brunswick"
    camden = "Camden"


@router.get(
    path="/schedules",
    status_code=status.HTTP_200_OK,
    tags=["Schedule Generator"],
    response_model=Schedule,
)
async def get_schedules(year: str, term: Semesters, campus: Campuses):
    """Retrieves schedule of classes from Rutgers University's Schedule of Classes API"""
    schedule = RutgersScheduleOfClasses(year=year, term=term, campus=campus)

    classes = schedule.fetch_filtered_schedule_of_classes()

    return dict(response=classes)


@router.get(path="/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}
