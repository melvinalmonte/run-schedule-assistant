from enum import Enum
from pydantic import BaseModel
from typing import List


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
