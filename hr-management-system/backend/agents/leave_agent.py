"""
Leave Agent - Handles leave management queries with LLM enhancement.
"""
from typing import Dict, Optional
from datetime import datetime
from . import BaseAgent, format_date


class LeaveAgent(BaseAgent):
    """Agent for handling leave-related queries with LLM support."""
    
    KEYWORDS = [
        'leave', 'vacation', 'holiday', 'time off', 'pto', 'sick',
        'annual', 'personal', 'absence', 'day off', 'days off',
        'leave balance', 'request leave', 'cancel leave'
    ]
    
    def __init__(self):
        super().__init__(
            name="Leave Agent",
            description="Handles leave balance and request queries"
        )
        try:
            from llm_service import llm_service
            self.llm = llm_service
        except ImportError:
            self.llm = None
    
    def can_handle(self, query: str) -> bool:
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.KEYWORDS)
    
    def process(self, query: str, employee_id: str, context: Optional[Dict] = None) -> str:
        leaves_data = self.load_json_data("leaves.json")
        
        if employee_id not in leaves_data:
            return "❌ Sorry, I couldn't find your leave records."
        
        employee_leave = leaves_data[employee_id]
        
        # Try LLM response first
        if self.llm and self.llm.is_available():
            balance = employee_leave['balance']
            response = self.llm.generate_response(
                query=query,
                agent_name="Leave Agent",
                context_data={
                    "employee_name": employee_leave.get("employee_name"),
                    "leave_balance": {
                        "annual": {"total": balance['annual'], "used": balance['used_annual'], "remaining": balance['annual'] - balance['used_annual']},
                        "sick": {"total": balance['sick'], "used": balance['used_sick'], "remaining": balance['sick'] - balance['used_sick']},
                        "personal": {"total": balance['personal'], "used": balance['used_personal'], "remaining": balance['personal'] - balance['used_personal']}
                    },
                    "leave_requests": employee_leave.get("requests", [])
                },
                system_context="You are the Leave Agent. Help employees check leave balances, view leave history, and understand leave policies. Present data clearly with tables."
            )
            if response:
                return response
        
        # Fallback to rule-based response
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['balance', 'remaining', 'how many', 'available']):
            return self._get_leave_balance(employee_leave)
        elif any(word in query_lower for word in ['history', 'past', 'previous', 'taken']):
            return self._get_leave_history(employee_leave)
        elif any(word in query_lower for word in ['pending', 'status']):
            return self._get_pending_requests(employee_leave)
        else:
            return self._get_leave_balance(employee_leave)
    
    def _get_leave_balance(self, employee_leave: Dict) -> str:
        """Get current leave balance."""
        balance = employee_leave['balance']
        name = employee_leave['employee_name']
        
        annual_remaining = balance['annual'] - balance['used_annual']
        sick_remaining = balance['sick'] - balance['used_sick']
        personal_remaining = balance['personal'] - balance['used_personal']
        
        return f"""📅 **Leave Balance - {name}**

| Type | Total | Used | Remaining |
|------|-------|------|-----------|
| 🏖️ Annual | {balance['annual']} | {balance['used_annual']} | **{annual_remaining}** |
| 🤒 Sick | {balance['sick']} | {balance['used_sick']} | **{sick_remaining}** |
| 👤 Personal | {balance['personal']} | {balance['used_personal']} | **{personal_remaining}** |

**Total Available:** {annual_remaining + sick_remaining + personal_remaining} days"""
    
    def _get_leave_history(self, employee_leave: Dict) -> str:
        """Get leave request history."""
        requests = employee_leave.get('requests', [])
        
        if not requests:
            return "📋 No leave history found."
        
        response = f"📋 **Leave History - {employee_leave['employee_name']}**\n\n"
        response += "| Type | Dates | Days | Status |\n"
        response += "|------|-------|------|--------|\n"
        
        for req in requests:
            status_emoji = "✅" if req['status'] == 'approved' else ("⏳" if req['status'] == 'pending' else "❌")
            response += f"| {req['type'].title()} | {req['start_date']} to {req['end_date']} | {req['days']} | {status_emoji} |\n"
        
        return response
    
    def _get_pending_requests(self, employee_leave: Dict) -> str:
        """Get pending leave requests."""
        requests = employee_leave.get('requests', [])
        pending = [r for r in requests if r['status'] == 'pending']
        
        if not pending:
            return "✅ No pending leave requests."
        
        response = "⏳ **Pending Leave Requests**\n\n"
        for req in pending:
            response += f"- **{req['type'].title()}**: {req['start_date']} to {req['end_date']} ({req['days']} days)\n"
            response += f"  Reason: {req['reason']}\n\n"
        
        return response
