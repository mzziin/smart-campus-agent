"""
Chat endpoint - Handles student queries via AI agent.
"""
from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.agent import create_campus_agent

router = APIRouter(prefix="/chat", tags=["Chat"])

# Initialize agent (singleton pattern for efficiency)
_agent = None


def get_agent():
    """Get or create the campus agent instance"""
    global _agent
    if _agent is None:
        try:
            _agent = create_campus_agent()
        except ValueError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize AI agent: {str(e)}"
            )
    return _agent


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a student query using the AI agent.
    
    Args:
        request: ChatRequest with user message
        
    Returns:
        ChatResponse with AI-generated response and optional data
    """
    try:
        agent = get_agent()
        result = await agent.process_query(request.message)
        
        return ChatResponse(
            message=result["message"],
            data=result.get("data")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Campus Concierge - Chat Service"
    }