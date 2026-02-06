# AI Campus Concierge

A college-scoped AI assistant for campus events, exams, and placements.

## Architecture

```
campus-concierge/
├── backend/              # FastAPI backend + AI agent
│   ├── app/
│   │   ├── models/      # Pydantic models & DB schemas
│   │   ├── tools/       # Deterministic data access tools
│   │   ├── agent/       # Pydantic AI agent
│   │   ├── database/    # SQLite connection & initialization
│   │   ├── routes/      # FastAPI routes (chat + admin)
│   │   └── main.py      # FastAPI app entry point
│   └── requirements.txt
├── frontend/            # Streamlit UI
│   ├── app.py
│   └── requirements.txt
├── data/                # SQLite database
│   └── campus.db
└── README.md
```

## Tech Stack

- **LLM**: Groq (free tier) with Llama models
- **AI Framework**: Pydantic AI
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: SQLite

## Setup Instructions

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m app.database.init_db  # Initialize database with sample data
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 3. Access Points

- **Student Chat Interface**: http://localhost:8501
- **Admin Panel**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/docs

## Environment Variables

Create `.env` file in backend/:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get free API key from: https://console.groq.com/

## Supported Queries

### Events
- "What's happening today?"
- "Any cultural events this week?"
- "Technical events tomorrow?"

### Exams
- "When is the CSE semester 3 exam?"
- "Data Structures exam date?"
- "Exam schedule for semester 5 ECE"

### Placements
- "Any placement drives coming up?"
- "Placement drives for CSE students?"
- "Which companies are visiting this week?"