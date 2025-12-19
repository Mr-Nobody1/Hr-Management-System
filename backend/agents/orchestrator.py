"""
Orchestrator Agent - Routes queries to specialized agents using LLM intelligence.
"""
from typing import Dict, Optional, List, Tuple
from . import BaseAgent
from .employee_agent import EmployeeAgent
from .payslip_agent import PayslipAgent
from .leave_agent import LeaveAgent
from .attendance_agent import AttendanceAgent
from .benefits_agent import BenefitsAgent
from .performance_agent import PerformanceAgent
from .policy_agent import PolicyAgent


class OrchestratorAgent(BaseAgent):
    """Main agent that routes queries to specialized agents using Gemini LLM."""
    
    def __init__(self):
        super().__init__(
            name="HR Assistant",
            description="Main HR assistant that intelligently routes queries to specialized agents"
        )
        
        # Initialize all specialized agents
        self.agents = {
            "PAYSLIP": PayslipAgent(),
            "LEAVE": LeaveAgent(),
            "EMPLOYEE": EmployeeAgent(),
            "ATTENDANCE": AttendanceAgent(),
            "BENEFITS": BenefitsAgent(),
            "PERFORMANCE": PerformanceAgent(),
            "POLICY": PolicyAgent(),
        }
        
        # Import LLM service
        try:
            from llm_service import llm_service
            self.llm = llm_service
            self.llm_available = llm_service.is_available()
        except ImportError:
            self.llm = None
            self.llm_available = False
        
        # Fallback keyword matching (used when LLM is not available)
        self.agent_keywords = {
            "PAYSLIP": ['payslip', 'salary', 'pay', 'payment', 'wage', 'income', 'deduction', 'tax', 'gross', 'net', 'earnings'],
            "LEAVE": ['leave', 'vacation', 'holiday', 'time off', 'pto', 'sick', 'annual', 'personal', 'absence'],
            "EMPLOYEE": ['profile', 'employee', 'team', 'department', 'manager', 'coworker', 'colleague', 'who am i'],
            "ATTENDANCE": ['attendance', 'clock', 'check in', 'check out', 'hours', 'overtime', 'schedule', 'late'],
            "BENEFITS": ['benefit', 'insurance', 'health', 'medical', 'dental', '401k', 'retirement', 'wellness'],
            "PERFORMANCE": ['performance', 'review', 'rating', 'goals', 'goal', 'kpi', 'feedback', 'evaluation', 'appraisal'],
            "POLICY": ['policy', 'policies', 'rule', 'rules', 'guideline', 'wfh', 'work from home', 'dress code', 'faq'],
        }
        
        self.greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'greetings']
        self.help_keywords = ['help', 'what can you do', 'how can you help', 'options', 'commands']
    
    def can_handle(self, query: str) -> bool:
        """Orchestrator can always handle queries."""
        return True
    
    def _route_with_llm(self, query: str) -> Tuple[str, str, float]:
        """Route query using Gemini LLM intelligence."""
        if not self.llm_available:
            return None, None, 0.0
        
        result = self.llm.route_query(query)
        return result.get("agent"), result.get("intent"), result.get("confidence", 0.0)
    
    def _route_with_keywords(self, query: str) -> str:
        """Fallback keyword-based routing."""
        query_lower = query.lower()
        
        # Check for greetings
        if any(kw in query_lower for kw in self.greeting_keywords):
            return "GREETING"
        
        # Check for help
        if any(kw in query_lower for kw in self.help_keywords):
            return "HELP"
        
        # Check each agent's keywords
        for agent_name, keywords in self.agent_keywords.items():
            if any(kw in query_lower for kw in keywords):
                return agent_name
        
        return "GENERAL"
    
    def process(self, query: str, employee_id: str, context: Optional[Dict] = None) -> str:
        # Try LLM routing first
        agent_name, intent, confidence = self._route_with_llm(query)
        routing_method = "LLM"
        
        # If LLM routing failed or low confidence, use keyword fallback
        if not agent_name or confidence < 0.5:
            agent_name = self._route_with_keywords(query)
            intent = "keyword-matched"
            routing_method = "Keywords"
        
        print(f"🔀 Routing to {agent_name} via {routing_method} (intent: {intent}, confidence: {confidence})")
        
        # Handle greetings
        if agent_name == "GREETING" or agent_name == "GENERAL":
            query_lower = query.lower()
            if any(kw in query_lower for kw in self.greeting_keywords):
                return self._get_greeting(employee_id)
        
        # Handle help
        if agent_name == "HELP":
            return self._get_help()
        
        # Handle general queries
        if agent_name == "GENERAL":
            return self._handle_general_query(query, employee_id)
        
        # Route to specialized agent
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            return agent.process(query, employee_id, context)
        
        # Fallback
        return self._get_fallback_response(query)
    
    def _handle_general_query(self, query: str, employee_id: str) -> str:
        """Handle general HR queries using LLM."""
        if self.llm_available:
            employees = self.load_json_data("employees.json")
            current_employee = None
            for emp in employees:
                if emp["id"] == employee_id:
                    current_employee = emp
                    break
            
            context = {
                "employee": current_employee,
                "capabilities": {
                    "Payslip Agent": "Salary info, payslips, deductions, tax breakdown",
                    "Leave Agent": "Leave balance, vacation requests, PTO tracking",
                    "Employee Agent": "Profile, team members, department info",
                    "Attendance Agent": "Clock in/out, work hours, overtime",
                    "Benefits Agent": "Health insurance, 401k, wellness programs"
                }
            }
            
            response = self.llm.generate_response(
                query=query,
                agent_name="HR Assistant",
                context_data=context,
                system_context="You are the main HR Assistant. Answer general HR questions or guide users to ask about specific topics like payslips, leave, attendance, benefits, or their profile."
            )
            
            if response:
                return response
        
        return self._get_fallback_response(query)
    
    def _get_greeting(self, employee_id: str) -> str:
        """Return a greeting message."""
        try:
            employees = self.load_json_data("employees.json")
            name = "there"
            for emp in employees:
                if emp["id"] == employee_id:
                    name = emp["name"].split()[0]
                    break
        except:
            name = "there"
        
        llm_status = "🧠 **AI-Powered**" if self.llm_available else "📋 **Keyword-Based**"
        
        return f"""👋 **Hello, {name}!**

I'm your HR Assistant {llm_status}

{"I use **Gemini 2.5 Flash** to understand your requests naturally. Just ask me anything!" if self.llm_available else "I can help you with HR tasks using keyword matching."}

**What I can help you with:**
- 💰 **Payslip** - Salary, deductions, tax info
- 📅 **Leave** - Balance, requests, history
- 👤 **Profile** - Your info, team, department
- ⏰ **Attendance** - Clock in/out, hours
- 🎁 **Benefits** - Insurance, 401k, wellness

How can I assist you today? 🚀"""
    
    def _get_help(self) -> str:
        """Return help information."""
        return """🤖 **HR Assistant - Help**

{"**Powered by Gemini 2.5 Flash** - Ask naturally, I'll understand!" if self.llm_available else "Using keyword-based matching."}

### 💬 Example Questions

| Topic | Try Asking |
|-------|------------|
| 💰 Pay | "Show my payslip", "What's my salary?" |
| 📅 Leave | "How many days off do I have?", "Leave balance" |
| 👤 Profile | "Tell me about myself", "Who's on my team?" |
| ⏰ Time | "Clock in", "How many hours this week?" |
| 🎁 Benefits | "What insurance do I have?", "401k details" |

Just type your question! 💬"""
    
    def _get_fallback_response(self, query: str) -> str:
        """Return a fallback response when no agent matches."""
        return f"""🤔 **I'm not sure how to help with that**

I couldn't understand: *"{query}"*

**Try asking about:**
- 💰 Payslip & salary
- 📅 Leave & time off
- 👤 Your profile & team
- ⏰ Attendance & hours
- 🎁 Benefits & insurance

Type **"help"** for more examples!"""
    
    def get_agent_for_query(self, query: str) -> Tuple[str, str]:
        """Get the name of the agent that would handle this query."""
        agent_name, intent, confidence = self._route_with_llm(query)
        
        if not agent_name or confidence < 0.5:
            agent_name = self._route_with_keywords(query)
            
        if agent_name == "GREETING":
            return ("HR Assistant", "Greeting")
        if agent_name == "HELP":
            return ("HR Assistant", "Help")
        if agent_name == "GENERAL":
            return ("HR Assistant", "General Query")
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            return (agent.name, agent.description)
        
        return ("HR Assistant", "Fallback")
