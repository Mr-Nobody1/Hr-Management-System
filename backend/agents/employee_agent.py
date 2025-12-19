"""
Employee Agent - Handles employee information queries with LLM enhancement.
"""
from typing import Dict, Optional
from . import BaseAgent


class EmployeeAgent(BaseAgent):
    """Agent for handling employee-related queries with LLM support."""
    
    KEYWORDS = [
        'profile', 'employee', 'team', 'department', 'manager', 
        'coworker', 'colleague', 'who am i', 'my info', 'my information',
        'my details', 'contact', 'position', 'job', 'role', 'about me'
    ]
    
    def __init__(self):
        super().__init__(
            name="Employee Agent",
            description="Handles employee profile and team information queries"
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
        employees = self.load_json_data("employees.json")
        
        # Find current employee
        current_employee = None
        for emp in employees:
            if emp["id"] == employee_id:
                current_employee = emp
                break
        
        if not current_employee:
            return "❌ Sorry, I couldn't find your employee record."
        
        # Get team members
        team_members = []
        for emp in employees:
            if emp['id'] in current_employee.get('team', []):
                team_members.append({"name": emp['name'], "position": emp['position'], "email": emp['email']})
        
        # Get manager info
        manager_info = None
        if current_employee.get('manager_id'):
            for emp in employees:
                if emp['id'] == current_employee['manager_id']:
                    manager_info = {"name": emp['name'], "position": emp['position'], "email": emp['email']}
                    break
        
        # Try LLM response first
        if self.llm and self.llm.is_available():
            response = self.llm.generate_response(
                query=query,
                agent_name="Employee Agent",
                context_data={
                    "employee": current_employee,
                    "team_members": team_members,
                    "manager": manager_info
                },
                system_context="You are the Employee Agent. Help employees view their profile, learn about their team, and find colleague information. Present data in clear tables."
            )
            if response:
                return response
        
        # Fallback to rule-based response
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['team', 'coworker', 'colleague']):
            return self._get_team_info(current_employee, employees)
        elif any(word in query_lower for word in ['manager', 'boss']):
            return self._get_manager_info(current_employee, employees)
        elif any(word in query_lower for word in ['department']):
            return self._get_department_info(current_employee, employees)
        else:
            return self._get_profile_info(current_employee)
    
    def _get_profile_info(self, employee: Dict) -> str:
        """Get the employee's profile information."""
        return f"""👤 **Your Profile**

| Field | Information |
|-------|-------------|
| **Name** | {employee['name']} |
| **ID** | {employee['id']} |
| **Position** | {employee['position']} |
| **Department** | {employee['department']} |
| **Email** | {employee['email']} |
| **Phone** | {employee['phone']} |
| **Manager** | {employee['manager'] or 'N/A'} |
| **Joined** | {employee['join_date']} |"""
    
    def _get_team_info(self, employee: Dict, all_employees: list) -> str:
        """Get information about team members."""
        team_ids = employee.get('team', [])
        
        if not team_ids:
            return "👥 You don't have any direct team members."
        
        team_members = [emp for emp in all_employees if emp['id'] in team_ids]
        
        response = f"👥 **Your Team** ({len(team_members)} members)\n\n"
        response += "| Name | Position | Email |\n"
        response += "|------|----------|-------|\n"
        
        for member in team_members:
            response += f"| {member['name']} | {member['position']} | {member['email']} |\n"
        
        return response
    
    def _get_manager_info(self, employee: Dict, all_employees: list) -> str:
        """Get information about the employee's manager."""
        manager_id = employee.get('manager_id')
        
        if not manager_id:
            return "👔 You are at the top - no manager assigned."
        
        for emp in all_employees:
            if emp['id'] == manager_id:
                return f"""👔 **Your Manager**

| Field | Information |
|-------|-------------|
| **Name** | {emp['name']} |
| **Position** | {emp['position']} |
| **Email** | {emp['email']} |
| **Phone** | {emp['phone']} |"""
        
        return "❌ Manager information not found."
    
    def _get_department_info(self, employee: Dict, all_employees: list) -> str:
        """Get information about the department."""
        dept = employee['department']
        dept_members = [emp for emp in all_employees if emp['department'] == dept]
        
        response = f"🏢 **{dept} Department** ({len(dept_members)} members)\n\n"
        response += "| Name | Position |\n"
        response += "|------|----------|\n"
        
        for member in dept_members:
            marker = " ⭐" if member['id'] == employee['id'] else ""
            response += f"| {member['name']}{marker} | {member['position']} |\n"
        
        return response
