"""
Campus Concierge AI Agent using Pydantic AI.
This agent understands natural language queries and selects appropriate tools.
"""
import os
from typing import Optional, List, Dict, Any
from datetime import date
from pathlib import Path
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from dotenv import load_dotenv

from app.tools import (
    get_events,
    get_today_events,
    get_exams,
    get_placements
)

# Load environment variables from backend/.env regardless of CWD
_ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_ENV_PATH)



# System prompt for the AI agent
SYSTEM_PROMPT = """You are the AI Campus Concierge for a college campus.

Your ONLY responsibility is to help students find information about:
1. Campus Events (cultural and technical)
2. Examination Schedules
3. Placement Drives

CRITICAL RULES:
- You have access to ONLY the tools provided to you
- NEVER fabricate or guess information
- If no data is found, clearly state "No data found" with the appropriate context
- Always use tools to fetch data - never make up dates, times, or venues
- Format responses in a clear, friendly, student-oriented manner
- If a query is outside your scope (events, exams, placements), politely decline

TOOL USAGE GUIDELINES:
- For "today" or "what's happening today" → use get_today_events()
- For specific event categories → use get_events(category="cultural" or "technical")
- For exam queries → use get_exams() with department/semester/subject filters
- For placement queries → use get_placements() with department/company filters

Current date: {current_date}

Remember: Be helpful, accurate, and never make up information!
"""


class CampusAgent:
    """
    Wrapper class for the Pydantic AI agent.
    Manages agent lifecycle and provides a clean interface.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.1-8b-instant"):
        """
        Initialize the Campus Agent.
        
        Args:
            api_key: Groq API key (reads from env if not provided)
            model: Groq model to use
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Groq API key not found. Set GROQ_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.model_name = model
        
        # Initialize Groq model
        self.model = GroqModel(self.model_name)

        
        # Create agent with tools
        self.agent = Agent(
            model=self.model,
            system_prompt=SYSTEM_PROMPT.format(
                current_date=date.today().strftime("%Y-%m-%d (%A)")
            ),
            tools=[
                get_today_events,
                get_events,
                get_exams,
                get_placements
            ],
            retries=2
        )
    
    async def process_query(self, user_message: str) -> Dict[str, Any]:
        """
        Process a user query and return structured response.
        """
        try:
            # Run the agent
            result = await self.agent.run(user_message)

            # ✅ CORRECT: Extract agent output
            output = result.output

            # Output is expected to be a dict like:
            # { "message": "...", "data": [...] }

            if isinstance(output, dict):
                return {
                    "message": output.get("message", ""),
                    "data": output.get("data")
                }

            # Fallback (defensive)
            return {
                "message": str(output),
                "data": None
            }

        except Exception as e:
            return {
                "message": f"I apologize, but I encountered an error: {str(e)}",
                "data": None
            }

    
    def _extract_tool_data(self, result) -> Optional[List[Dict]]:
        """
        Extract structured data from tool call results.
        
        Args:
            result: Agent run result
            
        Returns:
            List of data dictionaries or None
        """
        # This is a placeholder - Pydantic AI result structure may vary
        # Adjust based on actual result object structure
        try:
            # Check if result has tool call information
            if hasattr(result, 'all_messages'):
                for message in result.all_messages():
                    if hasattr(message, 'parts'):
                        for part in message.parts:
                            if hasattr(part, 'tool_return') and part.tool_return:
                                data = part.tool_return
                                if isinstance(data, list) and len(data) > 0:
                                    return data
            return None
        except Exception:
            return None


def create_campus_agent(api_key: Optional[str] = None) -> CampusAgent:
    """
    Factory function to create a CampusAgent instance.
    
    Args:
        api_key: Optional Groq API key
        
    Returns:
        Configured CampusAgent instance
    """
    return CampusAgent(api_key=api_key)


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        """Test the agent with sample queries"""
        agent = create_campus_agent()
        
        test_queries = [
            "What's happening today?",
            "Any technical events this week?",
            "When is the CSE semester 3 exam?",
            "Are there any placement drives coming up?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            response = await agent.process_query(query)
            print(f"💬 Response: {response['message']}")
            if response['data']:
                print(f"📊 Data: {response['data']}")
            print("-" * 80)
    
    # Run test
    asyncio.run(test_agent())