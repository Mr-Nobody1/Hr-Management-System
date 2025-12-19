"""
Attendance Agent - Handles attendance tracking queries with LLM enhancement.
"""
from typing import Dict, Optional
from datetime import datetime
from . import BaseAgent


class AttendanceAgent(BaseAgent):
    """Agent for handling attendance-related queries with LLM support."""
    
    KEYWORDS = [
        'attendance', 'clock', 'time', 'check in', 'check out', 
        'late', 'overtime', 'hours', 'work hours', 'working hours',
        'punch', 'present', 'absent', 'schedule'
    ]
    
    def __init__(self):
        super().__init__(
            name="Attendance Agent",
            description="Handles attendance tracking and time queries"
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
        attendance_data = self.load_json_data("attendance.json")
        
        if employee_id not in attendance_data:
            return "❌ Sorry, I couldn't find your attendance records."
        
        employee_attendance = attendance_data[employee_id]
        
        # Try LLM response first
        if self.llm and self.llm.is_available():
            response = self.llm.generate_response(
                query=query,
                agent_name="Attendance Agent",
                context_data={
                    "employee_name": employee_attendance.get("employee_name"),
                    "work_schedule": employee_attendance.get("work_schedule"),
                    "recent_records": employee_attendance.get("records", [])[:7],
                    "monthly_summary": employee_attendance.get("summary"),
                    "current_time": datetime.now().strftime("%Y-%m-%d %H:%M")
                },
                system_context="You are the Attendance Agent. Help employees track attendance, clock in/out, view work hours, and check overtime. For clock in/out requests, simulate the action and confirm."
            )
            if response:
                return response
        
        # Fallback to rule-based response
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['clock in', 'check in', 'punch in']):
            return self._clock_in(employee_attendance)
        elif any(word in query_lower for word in ['clock out', 'check out', 'punch out']):
            return self._clock_out(employee_attendance)
        elif any(word in query_lower for word in ['summary', 'total', 'month']):
            return self._get_summary(employee_attendance)
        elif any(word in query_lower for word in ['overtime']):
            return self._get_overtime(employee_attendance)
        else:
            return self._get_today_status(employee_attendance)
    
    def _clock_in(self, attendance: Dict) -> str:
        """Simulate clock in."""
        current_time = datetime.now().strftime("%H:%M")
        schedule = attendance['work_schedule']
        
        return f"""⏰ **Clock In Recorded**

| Detail | Value |
|--------|-------|
| **Date** | {datetime.now().strftime('%Y-%m-%d')} |
| **Time** | {current_time} |
| **Scheduled** | {schedule['start_time']} |
| **Status** | {'✅ On Time' if current_time <= schedule['start_time'] else '⚠️ Late'} |

Have a productive day! 🚀"""
    
    def _clock_out(self, attendance: Dict) -> str:
        """Simulate clock out."""
        current_time = datetime.now().strftime("%H:%M")
        
        return f"""⏰ **Clock Out Recorded**

| Detail | Value |
|--------|-------|
| **Date** | {datetime.now().strftime('%Y-%m-%d')} |
| **Time** | {current_time} |

See you tomorrow! 👋"""
    
    def _get_summary(self, attendance: Dict) -> str:
        """Get monthly attendance summary."""
        summary = attendance['summary']
        
        return f"""📊 **Attendance Summary - {summary['month']} {summary['year']}**

| Metric | Value |
|--------|-------|
| ✅ Days Present | {summary['total_days_present']} |
| ⚠️ Days Late | {summary['total_days_late']} |
| ❌ Days Absent | {summary['total_days_absent']} |
| ⏱️ Hours Worked | {summary['total_hours_worked']} hrs |
| 🌙 Overtime | {summary['total_overtime']} hrs |"""
    
    def _get_overtime(self, attendance: Dict) -> str:
        """Get overtime information."""
        summary = attendance['summary']
        records = attendance['records']
        
        response = f"🌙 **Overtime - {summary['month']} {summary['year']}**\n\n"
        response += f"**Total:** {summary['total_overtime']} hours\n\n"
        response += "| Date | Hours Worked | Overtime |\n"
        response += "|------|--------------|----------|\n"
        
        for record in records[:5]:
            if record.get('overtime', 0) > 0:
                response += f"| {record['date']} | {record['hours_worked']} | +{record['overtime']} |\n"
        
        return response
    
    def _get_today_status(self, attendance: Dict) -> str:
        """Get today's attendance status."""
        schedule = attendance['work_schedule']
        
        return f"""📍 **Attendance Status**

**Schedule:**
- Start: {schedule['start_time']}
- End: {schedule['end_time']}
- Days: {', '.join(schedule['work_days'])}

Would you like to **clock in** or **clock out**?"""
