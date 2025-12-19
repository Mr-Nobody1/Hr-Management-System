"""
Session Memory - In-memory conversation storage for multi-turn conversations.
"""
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


class SessionMemory:
    """In-memory session storage for conversation history."""
    
    def __init__(self, max_history: int = 10):
        """
        Initialize session memory.
        
        Args:
            max_history: Maximum number of messages to keep per session
        """
        self.sessions: Dict[str, List[Dict]] = defaultdict(list)
        self.max_history = max_history
    
    def add_message(self, session_id: str, role: str, content: str, agent_name: Optional[str] = None) -> None:
        """
        Add a message to the session history.
        
        Args:
            session_id: Unique session identifier
            role: Message role ('user' or 'assistant')
            content: Message content
            agent_name: Name of the agent that responded (for assistant messages)
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        if agent_name and role == "assistant":
            message["agent_name"] = agent_name
        
        self.sessions[session_id].append(message)
        
        # Trim to max history
        if len(self.sessions[session_id]) > self.max_history:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history:]
    
    def get_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Unique session identifier
            limit: Optional limit on number of messages to return
        
        Returns:
            List of message dictionaries
        """
        history = self.sessions.get(session_id, [])
        if limit:
            return history[-limit:]
        return history
    
    def get_context_string(self, session_id: str, limit: int = 5) -> str:
        """
        Get conversation history as a formatted string for LLM context.
        
        Args:
            session_id: Unique session identifier
            limit: Number of recent messages to include
        
        Returns:
            Formatted conversation history string
        """
        history = self.get_history(session_id, limit)
        
        if not history:
            return ""
        
        context_parts = ["Previous conversation:"]
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"]
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def clear_session(self, session_id: str) -> None:
        """
        Clear all history for a session.
        
        Args:
            session_id: Unique session identifier
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def get_all_sessions(self) -> List[str]:
        """Get list of all active session IDs."""
        return list(self.sessions.keys())
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        return session_id in self.sessions


# Singleton instance
session_memory = SessionMemory()
