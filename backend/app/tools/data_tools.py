"""
Deterministic data access tools.
These tools are called by the AI agent to retrieve structured data.
No LLM logic here - pure data access.
"""
from datetime import date, timedelta
from typing import List, Dict, Optional
from app.database import get_db_connection
from pathlib import Path
import json


def get_events(
    event_date: Optional[str] = None,
    category: Optional[str] = None,
    days_ahead: int = 7
) -> List[Dict]:
    """
    Retrieve campus events with optional filters.
    
    Args:
        event_date: Specific date in YYYY-MM-DD format (optional)
        category: Filter by 'cultural' or 'technical' (optional)
        days_ahead: Number of days to look ahead from today (default: 7)
    
    Returns:
        List of event dictionaries
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Base query
        query = "SELECT * FROM events WHERE 1=1"
        params = []
        
        # Date filtering
        if event_date:
            query += " AND date = ?"
            params.append(event_date)
        else:
            # Show events from today to N days ahead
            today = date.today().isoformat()
            future_date = (date.today() + timedelta(days=days_ahead)).isoformat()
            query += " AND date >= ? AND date <= ?"
            params.extend([today, future_date])
        
        # Category filtering
        if category and category in ['cultural', 'technical']:
            query += " AND category = ?"
            params.append(category)
        
        # Order by date and time
        query += " ORDER BY date ASC, time ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

import sqlite3
from pathlib import Path


def get_today_events() -> List[Dict]:
    """
    Return events happening today from SQLite database.
    """
    try:
        today = date.today().isoformat()

        DB_PATH = Path(__file__).resolve().parent.parent / "campus.db"

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # IMPORTANT
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, title, category, date, time, venue, organizer
            FROM events
            WHERE date = ?
            """,
            (today,)
        )

        rows = cursor.fetchall()
        conn.close()

        # Convert sqlite3.Row → dict
        return [dict(row) for row in rows]

    except Exception as e:
        print("🔥 get_today_events SQLite ERROR:", repr(e))
        raise



def get_exams(
    department: Optional[str] = None,
    semester: Optional[int] = None,
    subject: Optional[str] = None,
    days_ahead: int = 30
) -> List[Dict]:
    """
    Retrieve exam schedules with optional filters.
    
    Args:
        department: Filter by department code (CSE, ECE, etc.)
        semester: Filter by semester number (1-8)
        subject: Filter by subject name (partial match)
        days_ahead: Number of days to look ahead (default: 30)
    
    Returns:
        List of exam dictionaries
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Base query
        query = "SELECT * FROM exams WHERE 1=1"
        params = []
        
        # Date filtering (future exams only)
        today = date.today().isoformat()
        future_date = (date.today() + timedelta(days=days_ahead)).isoformat()
        query += " AND date >= ? AND date <= ?"
        params.extend([today, future_date])
        
        # Department filtering
        if department and department in ['CSE', 'ECE', 'ME', 'CE', 'IT', 'EEE']:
            query += " AND department = ?"
            params.append(department)
        
        # Semester filtering
        if semester and 1 <= semester <= 8:
            query += " AND semester = ?"
            params.append(semester)
        
        # Subject filtering (case-insensitive partial match)
        if subject:
            query += " AND LOWER(subject) LIKE LOWER(?)"
            params.append(f"%{subject}%")
        
        # Order by date and time
        query += " ORDER BY date ASC, time ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]


def get_placements(
    department: Optional[str] = None,
    company: Optional[str] = None,
    days_ahead: int = 30
) -> List[Dict]:
    """
    Retrieve placement drives with optional filters.
    
    Args:
        department: Filter by department code (CSE, ECE, etc.)
        company: Filter by company name (partial match)
        days_ahead: Number of days to look ahead (default: 30)
    
    Returns:
        List of placement dictionaries
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Base query
        query = "SELECT * FROM placements WHERE 1=1"
        params = []
        
        # Date filtering (future placements only)
        today = date.today().isoformat()
        future_date = (date.today() + timedelta(days=days_ahead)).isoformat()
        query += " AND date >= ? AND date <= ?"
        params.extend([today, future_date])
        
        # Department filtering (check if department is in comma-separated list)
        if department:
            query += " AND department LIKE ?"
            params.append(f"%{department}%")
        
        # Company filtering (case-insensitive partial match)
        if company:
            query += " AND LOWER(company) LIKE LOWER(?)"
            params.append(f"%{company}%")
        
        # Order by date and time
        query += " ORDER BY date ASC, time ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Parse department field (comma-separated to list)
        results = []
        for row in rows:
            result = dict(row)
            result['department'] = [d.strip() for d in result['department'].split(',')]
            results.append(result)
        
        return results


# Tool metadata for AI agent
TOOLS_METADATA = {
    "get_events": {
        "description": "Retrieve campus events (cultural or technical)",
        "parameters": {
            "event_date": "Specific date (YYYY-MM-DD) or None for upcoming events",
            "category": "'cultural' or 'technical' or None for all",
            "days_ahead": "Number of days to look ahead (default: 7)"
        }
    },
    "get_today_events": {
        "description": "Quick access to today's events",
        "parameters": {}
    },
    "get_exams": {
        "description": "Retrieve exam schedules",
        "parameters": {
            "department": "Department code (CSE, ECE, ME, CE, IT, EEE) or None",
            "semester": "Semester number (1-8) or None",
            "subject": "Subject name (partial match) or None",
            "days_ahead": "Number of days to look ahead (default: 30)"
        }
    },
    "get_placements": {
        "description": "Retrieve placement drive information",
        "parameters": {
            "department": "Department code or None",
            "company": "Company name (partial match) or None",
            "days_ahead": "Number of days to look ahead (default: 30)"
        }
    }
}