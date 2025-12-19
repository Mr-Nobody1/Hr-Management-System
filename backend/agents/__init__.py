"""
Base agent class and utilities for the HR Management System.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
from pathlib import Path


class BaseAgent(ABC):
    """Abstract base class for all HR agents."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.data_path = Path(__file__).parent.parent / "data"
    
    def load_json_data(self, filename: str) -> Dict:
        """Load data from a JSON file."""
        file_path = self.data_path / filename
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @abstractmethod
    def process(self, query: str, employee_id: str, context: Optional[Dict] = None) -> str:
        """Process a user query and return a response."""
        pass
    
    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """Check if this agent can handle the given query."""
        pass


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def format_date(date_str: str) -> str:
    """Format a date string for display."""
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except ValueError:
        return date_str
