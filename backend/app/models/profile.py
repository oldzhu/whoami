from pydantic import BaseModel
from typing import Optional, List


class Project(BaseModel):
    name: str
    description: str
    technologies: List[str]
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Experience(BaseModel):
    company: str
    role: str
    description: str
    start_date: str
    end_date: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: str
    field: str
    year: int


class Skill(BaseModel):
    name: str
    category: str
    level: int


class PersonalProfile(BaseModel):
    name: str
    title: str
    summary: str
    skills: List[str]
    projects: List[Project]
    experience: List[Experience]
    education: List[Education]
