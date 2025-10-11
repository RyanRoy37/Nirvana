from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    age: int
    occupation: str
    organisation: str
    interests: str | None = None
    email: EmailStr
    password: str

class ProjectCreate(BaseModel):
    title: str
    description: str
    tech_stack: str | None = None
    features:Optional[list[str]] = []
    prerequisites:Optional[list[str]] = []
    extra_info:Optional[str] = ""
    attachments:Optional[list[str]] = []