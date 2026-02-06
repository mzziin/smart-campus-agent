"""
Admin routes - Non-AI data management interface.
Simple HTML forms for CRUD operations.
"""
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import date

from app.database import get_db_connection
from app.models import EventCreate, ExamCreate, PlacementCreate

router = APIRouter(prefix="/admin", tags=["Admin"])

# Setup Jinja2 templates
TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
TEMPLATE_DIR.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@router.get("/", response_class=HTMLResponse)
async def admin_home(request: Request):
    """Admin panel home page with navigation"""
    return templates.TemplateResponse("admin_home.html", {"request": request})


# ==================== EVENT ROUTES ====================

@router.get("/events", response_class=HTMLResponse)
async def list_events(request: Request):
    """Display all events with add/delete options"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events ORDER BY date DESC")
        events = [dict(row) for row in cursor.fetchall()]
    
    return templates.TemplateResponse(
        "events.html",
        {"request": request, "events": events}
    )


@router.get("/events/add", response_class=HTMLResponse)
async def add_event_form(request: Request):
    """Display form to add new event"""
    return templates.TemplateResponse("add_event.html", {"request": request})


@router.post("/events/add")
async def add_event(
    title: str = Form(...),
    category: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    venue: str = Form(...),
    organizer: str = Form(...),
    description: str = Form("")
):
    """Add a new event to database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO events (title, category, date, time, venue, organizer, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, category, date, time, venue, organizer, description))
            conn.commit()
        
        return RedirectResponse(url="/admin/events", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding event: {str(e)}")


@router.post("/events/delete/{event_id}")
async def delete_event(event_id: int):
    """Delete an event"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
            conn.commit()
        
        return RedirectResponse(url="/admin/events", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting event: {str(e)}")


# ==================== EXAM ROUTES ====================

@router.get("/exams", response_class=HTMLResponse)
async def list_exams(request: Request):
    """Display all exams with add/delete options"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM exams ORDER BY date DESC")
        exams = [dict(row) for row in cursor.fetchall()]
    
    return templates.TemplateResponse(
        "exams.html",
        {"request": request, "exams": exams}
    )


@router.get("/exams/add", response_class=HTMLResponse)
async def add_exam_form(request: Request):
    """Display form to add new exam"""
    return templates.TemplateResponse("add_exam.html", {"request": request})


@router.post("/exams/add")
async def add_exam(
    exam_name: str = Form(...),
    subject: str = Form(...),
    department: str = Form(...),
    semester: int = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    venue: str = Form(...)
):
    """Add a new exam to database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO exams (exam_name, subject, department, semester, date, time, venue)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (exam_name, subject, department, semester, date, time, venue))
            conn.commit()
        
        return RedirectResponse(url="/admin/exams", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding exam: {str(e)}")


@router.post("/exams/delete/{exam_id}")
async def delete_exam(exam_id: int):
    """Delete an exam"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM exams WHERE id = ?", (exam_id,))
            conn.commit()
        
        return RedirectResponse(url="/admin/exams", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting exam: {str(e)}")


# ==================== PLACEMENT ROUTES ====================

@router.get("/placements", response_class=HTMLResponse)
async def list_placements(request: Request):
    """Display all placements with add/delete options"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM placements ORDER BY date DESC")
        placements = [dict(row) for row in cursor.fetchall()]
    
    return templates.TemplateResponse(
        "placements.html",
        {"request": request, "placements": placements}
    )


@router.get("/placements/add", response_class=HTMLResponse)
async def add_placement_form(request: Request):
    """Display form to add new placement"""
    return templates.TemplateResponse("add_placement.html", {"request": request})


@router.post("/placements/add")
async def add_placement(
    company: str = Form(...),
    role: str = Form(...),
    department: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    venue: str = Form(...)
):
    """Add a new placement to database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO placements (company, role, department, date, time, venue)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (company, role, department, date, time, venue))
            conn.commit()
        
        return RedirectResponse(url="/admin/placements", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding placement: {str(e)}")


@router.post("/placements/delete/{placement_id}")
async def delete_placement(placement_id: int):
    """Delete a placement"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM placements WHERE id = ?", (placement_id,))
            conn.commit()
        
        return RedirectResponse(url="/admin/placements", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting placement: {str(e)}")