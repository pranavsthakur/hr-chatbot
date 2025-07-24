from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    query: str

class Employee(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str
