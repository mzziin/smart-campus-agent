"""Tools package - Deterministic data access layer"""
from .data_tools import (
    get_events,
    get_today_events,
    get_exams,
    get_placements,
    TOOLS_METADATA
)

__all__ = [
    'get_events',
    'get_today_events',
    'get_exams',
    'get_placements',
    'TOOLS_METADATA'
]