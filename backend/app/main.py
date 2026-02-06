"""
Main FastAPI application entry point.
Combines chat and admin routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat_router, admin_router
from app.database import init_database

# Initialize database on startup
init_database()

# Create FastAPI app
app = FastAPI(
    title="AI Campus Concierge",
    description="College-scoped AI assistant for events, exams, and placements",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)
app.include_router(admin_router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "AI Campus Concierge",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "admin": "/admin",
            "docs": "/docs",
            "health": "/chat/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Campus Concierge"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )