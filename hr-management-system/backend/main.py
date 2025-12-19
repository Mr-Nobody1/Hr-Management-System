"""
HR Management System - FastAPI Backend
Main application entry point with API endpoints.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
from pathlib import Path

from models import ChatMessage, ChatResponse, Employee
from agents.orchestrator import OrchestratorAgent
from session_memory import session_memory
from translations import SUPPORTED_LANGUAGES, UI_TRANSLATIONS

# Initialize FastAPI app
app = FastAPI(
    title="HR Management System API",
    description="Multi-agent HR assistant backend with 8 specialized agents",
    version="2.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the orchestrator agent
orchestrator = OrchestratorAgent()

# Data path
DATA_PATH = Path(__file__).parent / "data"


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "online",
        "message": "HR Management System API",
        "version": "2.0.0",
        "agents": [
            "Orchestrator Agent",
            "Payslip Agent",
            "Leave Agent",
            "Employee Agent",
            "Attendance Agent",
            "Benefits Agent",
            "Performance Agent",
            "Policy Agent"
        ],
        "features": ["conversation_memory", "multi_language"]
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Process a chat message and return a response from the appropriate agent.
    Supports conversation memory and multi-language responses.
    """
    try:
        # Get conversation history for context
        conversation_history = session_memory.get_context_string(
            message.session_id, 
            limit=5
        )
        
        # Store user message
        session_memory.add_message(
            session_id=message.session_id,
            role="user",
            content=message.message
        )
        
        # Get agent info for this query
        agent_name, agent_desc = orchestrator.get_agent_for_query(message.message)
        
        # Process the message with context
        response = orchestrator.process(
            query=message.message,
            employee_id=message.employee_id,
            context={
                "language": message.language,
                "conversation_history": conversation_history
            }
        )
        
        # Store assistant response
        session_memory.add_message(
            session_id=message.session_id,
            role="assistant",
            content=response,
            agent_name=agent_name
        )
        
        return ChatResponse(
            response=response,
            agent_name=agent_name,
            agent_description=agent_desc,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/employees")
async def get_employees():
    """Get all employees."""
    try:
        with open(DATA_PATH / "employees.json", "r") as f:
            employees = json.load(f)
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/employees/{employee_id}")
async def get_employee(employee_id: str):
    """Get a specific employee by ID."""
    try:
        with open(DATA_PATH / "employees.json", "r") as f:
            employees = json.load(f)
        
        for emp in employees:
            if emp["id"] == employee_id:
                return emp
        
        raise HTTPException(status_code=404, detail="Employee not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/languages")
async def get_languages():
    """Get available languages for the UI."""
    return {
        "languages": SUPPORTED_LANGUAGES,
        "default": "en"
    }


@app.get("/api/translations/{language_code}")
async def get_translations(language_code: str):
    """Get UI translations for a specific language."""
    if language_code not in UI_TRANSLATIONS:
        language_code = "en"
    return UI_TRANSLATIONS[language_code]


@app.delete("/api/session/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session."""
    session_memory.clear_session(session_id)
    return {"message": f"Session {session_id} cleared"}


@app.get("/api/agents")
async def get_agents():
    """Get information about available agents."""
    return {
        "agents": [
            {
                "name": "Orchestrator Agent",
                "description": "Routes queries to specialized agents",
                "type": "router"
            },
            {
                "name": "Payslip Agent",
                "description": "Handles salary and payslip queries",
                "keywords": ["payslip", "salary", "pay", "deduction", "tax"]
            },
            {
                "name": "Leave Agent",
                "description": "Handles leave balance and requests",
                "keywords": ["leave", "vacation", "time off", "sick", "pto"]
            },
            {
                "name": "Employee Agent",
                "description": "Handles profile and team queries",
                "keywords": ["profile", "team", "department", "manager"]
            },
            {
                "name": "Attendance Agent",
                "description": "Handles attendance tracking",
                "keywords": ["attendance", "clock", "hours", "overtime"]
            },
            {
                "name": "Benefits Agent",
                "description": "Handles benefits enrollment queries",
                "keywords": ["benefits", "insurance", "401k", "health"]
            },
            {
                "name": "Performance Agent",
                "description": "Handles performance reviews and goals",
                "keywords": ["performance", "review", "goals", "kpi", "rating"]
            },
            {
                "name": "Policy Agent",
                "description": "Handles HR policies and FAQs",
                "keywords": ["policy", "rules", "guidelines", "wfh", "faq"]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
