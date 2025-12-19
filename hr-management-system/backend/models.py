"""
Pydantic models for the HR Management System.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    """Model for incoming chat messages."""
    message: str
    employee_id: str = "EMP001"  # Default to first employee for demo
    session_id: str = "default"  # Session ID for conversation memory
    language: str = "en"  # Language code (en, es, fr, ar, zh)


class ChatResponse(BaseModel):
    """Model for chat responses."""
    response: str
    agent_name: str
    agent_description: str
    timestamp: str


class Employee(BaseModel):
    """Model for employee data."""
    id: str
    name: str
    email: str
    department: str
    position: str
    manager: Optional[str]
    manager_id: Optional[str]
    join_date: str
    phone: str
    salary: float
    team: List[str] = []
