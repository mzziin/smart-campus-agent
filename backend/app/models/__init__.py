"""Models package"""
from .Schemas import (
    Event, EventCreate,
    Exam, ExamCreate,
    Placement, PlacementCreate,
    ChatRequest, ChatResponse
)

__all__ = [
    'Event', 'EventCreate',
    'Exam', 'ExamCreate', 
    'Placement', 'PlacementCreate',
    'ChatRequest', 'ChatResponse'
]