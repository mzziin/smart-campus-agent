"""
AI Campus Concierge - Student Chat Interface
Streamlit frontend for querying campus information.
"""
import streamlit as st
import requests
from datetime import datetime
from typing import Optional, Dict, Any

# Configuration
BACKEND_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat/"

# Page configuration
st.set_page_config(
    page_title="AI Campus Concierge",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        margin-left: 20%;
    }
    
    .assistant-message {
        background: #f8f9fa;
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        margin-right: 20%;
        border-left: 4px solid #667eea;
    }
    
    .data-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .data-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
    }
    
    .quick-action {
        background: white;
        border: 2px solid #667eea;
        color: #667eea;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .quick-action:hover {
        background: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def send_message(message: str) -> Optional[Dict[str, Any]]:
    """
    Send message to backend and get response.
    
    Args:
        message: User query
        
    Returns:
        Response dictionary or None if error
    """
    try:
        response = requests.post(
            CHAT_ENDPOINT,
            json={"message": message},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timeout. The AI is taking too long to respond.")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


def display_data_card(item: Dict[str, Any], item_type: str):
    """
    Display a single data item as a card.
    
    Args:
        item: Data dictionary
        item_type: Type of data (event, exam, placement)
    """
    with st.container():
        if item_type == "event":
            st.markdown(f"""
            <div class="data-card">
                <h4 style="margin: 0 0 10px 0; color: #667eea;">📅 {item.get('title', 'N/A')}</h4>
                <p style="margin: 5px 0;"><strong>Category:</strong> {item.get('category', 'N/A').title()}</p>
                <p style="margin: 5px 0;"><strong>Date:</strong> {item.get('date', 'N/A')} at {item.get('time', 'N/A')}</p>
                <p style="margin: 5px 0;"><strong>Venue:</strong> {item.get('venue', 'N/A')}</p>
                <p style="margin: 5px 0;"><strong>Organizer:</strong> {item.get('organizer', 'N/A')}</p>
                {f"<p style='margin: 5px 0; color: #6c757d;'>{item.get('description', '')}</p>" if item.get('description') else ''}
            </div>
            """, unsafe_allow_html=True)
            
        elif item_type == "exam":
            st.markdown(f"""
            <div class="data-card">
                <h4 style="margin: 0 0 10px 0; color: #f5576c;">📝 {item.get('subject', 'N/A')}</h4>
                <p style="margin: 5px 0;"><strong>Exam:</strong> {item.get('exam_name', 'N/A')}</p>
                <p style="margin: 5px 0;"><strong>Department:</strong> {item.get('department', 'N/A')} - Semester {item.get('semester', 'N/A')}</p>
                <p style="margin: 5px 0;"><strong>Date:</strong> {item.get('date', 'N/A')} at {item.get('time', 'N/A')}</p>
                <p style="margin: 5px 0;"><strong>Venue:</strong> {item.get('venue', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif item_type == "placement":
            departments = item.get('department', [])
            dept_str = ', '.join(departments) if isinstance(departments, list) else departments
            st.markdown(f"""
            <div class="data-card">
                <h4 style="margin: 0 0 10px 0; color: #00f2fe;">💼 {item.get('company', 'N/A')}</h4>
                <p style="margin: 5px 0;"><strong>Role:</strong> {item.get('role', 'N/A')}</p>
                <p style="margin: 5px 0;"><strong>Eligible:</strong> {dept_str}</p>
                <p style="margin: 5px 0;"><strong>Date:</strong> {item.get('date', 'N/A')} at {item.get('time', 'N/A')}</p>
                <p style="margin: 5px 0;"><strong>Venue:</strong> {item.get('venue', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0


def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 3rem; margin-bottom: 0.5rem;">
            🎓 AI Campus Concierge
        </h1>
        <p style="color: #6c757d; font-size: 1.2rem;">
            Your smart assistant for campus events, exams, and placements
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🚀 Quick Actions")
        
        quick_queries = [
            "Any technical events this week?",
            "Show me cultural events",
            "When is the CSE semester 3 exam?",
            "Any placement drives coming up?",
            "Placement drives for CSE students"
        ]
        
        st.markdown("Click to ask:")
        for query in quick_queries:
            if st.button(query, key=f"quick_{query}"):
                st.session_state.quick_query = query
        
        st.markdown("---")
        st.markdown("### ℹ️ What I Can Help With")
        st.markdown("""
        - 📅 **Events**: Cultural & technical campus events
        - 📝 **Exams**: Examination schedules by department/semester
        - 💼 **Placements**: Upcoming placement drives
        """)
        
        st.markdown("---")
        st.markdown("### 🔗 Quick Links")
        st.markdown(f"[📊 Admin Panel]({BACKEND_URL}/admin)")
        st.markdown(f"[📖 API Docs]({BACKEND_URL}/docs)")
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.message_count = 0
            st.rerun()
    
    # Main chat area
    st.markdown("### 💬 Chat")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>🤖 Assistant:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
                
                # Display structured data if available
                if msg.get('data'):
                    st.markdown("---")
                    for item in msg['data']:
                        # Infer type from data structure
                        if 'category' in item:
                            display_data_card(item, "event")
                        elif 'semester' in item:
                            display_data_card(item, "exam")
                        elif 'company' in item:
                            display_data_card(item, "placement")
    
    # Chat input
    st.markdown("---")
    
    # Handle quick query from sidebar
    if 'quick_query' in st.session_state:
        user_input = st.session_state.quick_query
        del st.session_state.quick_query
    else:
        user_input = st.chat_input("Ask me about events, exams, or placements...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Show thinking indicator
        with st.spinner("🤔 Thinking..."):
            # Send to backend
            response = send_message(user_input)
        
        if response:
            # Add assistant response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.get("message", "Sorry, I couldn't generate a response."),
                "data": response.get("data")
            })
            st.session_state.message_count += 1
        
        # Rerun to update chat
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <p>💡 <strong>Tip:</strong> Try asking "What's happening today?" or "Any CSE exams this week?"</p>
        <p style="font-size: 0.9rem;">Made with ❤️ using Streamlit & FastAPI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()