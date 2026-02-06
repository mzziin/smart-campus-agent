"""
Pydantic models for data validation and API schemas.
These models ensure type safety and schema validation.
"""
from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel, Field


class EventBase(BaseModel):
    """Base model for Event entity"""
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., pattern="^(cultural|technical)$")
    date: date
    time: str = Field(..., description="Time in HH:MM AM/PM format")
    venue: str = Field(..., min_length=1, max_length=200)
    organizer: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)


class EventCreate(EventBase):
    """Model for creating new events"""
    pass


class Event(EventBase):
    """Complete Event model with ID"""
    id: int

    class Config:
        from_attributes = True


class ExamBase(BaseModel):
    """Base model for Exam entity"""
    exam_name: str = Field(..., min_length=1, max_length=200)
    subject: str = Field(..., min_length=1, max_length=200)
    department: str = Field(..., pattern="^(CSE|ECE|ME|CE|IT|EEE)$")
    semester: int = Field(..., ge=1, le=8)
    date: date
    time: str = Field(..., description="Time in HH:MM AM/PM format")
    venue: str = Field(..., min_length=1, max_length=200)


class ExamCreate(ExamBase):
    """Model for creating new exams"""
    pass


class Exam(ExamBase):
    """Complete Exam model with ID"""
    id: int

    class Config:
        from_attributes = True


class PlacementBase(BaseModel):
    """Base model for Placement entity"""
    company: str = Field(..., min_length=1, max_length=200)
    role: str = Field(..., min_length=1, max_length=200)
    department: str = Field(..., description="Comma-separated departments, e.g., 'CSE,IT,ECE'")
    date: date
    time: str = Field(..., description="Time in HH:MM AM/PM format")
    venue: str = Field(..., min_length=1, max_length=200)


class PlacementCreate(PlacementBase):
    """Model for creating new placements"""
    pass


class Placement(PlacementBase):
    """Complete Placement model with ID"""
    id: int

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    message: str
    data: Optional[List[dict]] = None