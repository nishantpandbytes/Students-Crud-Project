from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

# Base schema (common fields)
class StudentBase(BaseModel):
    name: str
    dob: date
    contact: str
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

# Create request schema (POST /students)
class StudentCreate(StudentBase):
    pass

# Update request schema (PUT/PATCH /students/{id})
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    contact: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

# Response schema (API Output ke liye)
class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True