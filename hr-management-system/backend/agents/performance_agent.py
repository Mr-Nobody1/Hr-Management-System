"""
Performance Agent - Handles performance review and goal queries with LLM enhancement.
"""
from typing import Dict, Optional
from . import BaseAgent


class PerformanceAgent(BaseAgent):
    """Agent for handling performance-related queries with LLM support."""
    
    KEYWORDS = [
        'performance', 'review', 'rating', 'goals', 'goal', 'kpi',
        'feedback', 'evaluation', 'appraisal', 'improvement',
        'strengths', 'weaknesses', 'objectives', 'targets'
    ]
    
    def __init__(self):
        super().__init__(
            name="Performance Agent",
            description="Handles performance reviews, goals, and KPI queries"
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
        performance_data = self.load_json_data("performance.json")
        
        if employee_id not in performance_data:
            return "❌ Sorry, I couldn't find your performance records."
        
        employee_perf = performance_data[employee_id]
        
        # Try LLM response first
        if self.llm and self.llm.is_available():
            response = self.llm.generate_response(
                query=query,
                agent_name="Performance Agent",
                context_data={
                    "employee_name": employee_perf.get("employee_name"),
                    "current_rating": employee_perf.get("current_rating"),
                    "last_review_date": employee_perf.get("last_review_date"),
                    "next_review_date": employee_perf.get("next_review_date"),
                    "reviews": employee_perf.get("reviews", []),
                    "goals": employee_perf.get("goals", []),
                    "kpis": employee_perf.get("kpis", {}),
                    "recent_feedback": employee_perf.get("recent_feedback", [])
                },
                system_context="You are the Performance Agent. Help employees view their performance reviews, track goals, understand KPIs, and see feedback. Present data clearly with tables and progress indicators."
            )
            if response:
                return response
        
        # Fallback to rule-based response
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['goal', 'objective', 'target']):
            return self._get_goals(employee_perf)
        elif any(word in query_lower for word in ['kpi', 'metric', 'score']):
            return self._get_kpis(employee_perf)
        elif any(word in query_lower for word in ['feedback', 'comment']):
            return self._get_feedback(employee_perf)
        else:
            return self._get_performance_summary(employee_perf)
    
    def _get_performance_summary(self, employee_perf: Dict) -> str:
        """Get overall performance summary."""
        name = employee_perf['employee_name']
        rating = employee_perf['current_rating']
        last_review = employee_perf['last_review_date']
        next_review = employee_perf['next_review_date']
        
        # Rating emoji
        if rating >= 4.5:
            rating_emoji = "🌟"
            rating_text = "Exceptional"
        elif rating >= 4.0:
            rating_emoji = "⭐"
            rating_text = "Exceeds Expectations"
        elif rating >= 3.5:
            rating_emoji = "✅"
            rating_text = "Meets Expectations"
        else:
            rating_emoji = "📈"
            rating_text = "Developing"
        
        # Get latest review
        reviews = employee_perf.get('reviews', [])
        latest_review = reviews[0] if reviews else None
        
        response = f"""📊 **Performance Summary - {name}**

### Current Rating: {rating}/5.0 {rating_emoji}
**Status:** {rating_text}

| Metric | Value |
|--------|-------|
| 📅 Last Review | {last_review} |
| 📅 Next Review | {next_review} |

"""
        
        if latest_review:
            response += f"""### Latest Review ({latest_review['period']})
> {latest_review['summary']}

**Strengths:** {', '.join(latest_review.get('strengths', []))}
**Areas to Improve:** {', '.join(latest_review.get('areas_for_improvement', []))}
"""
        
        return response
    
    def _get_goals(self, employee_perf: Dict) -> str:
        """Get current goals."""
        goals = employee_perf.get('goals', [])
        name = employee_perf['employee_name']
        
        if not goals:
            return "📋 No goals found for the current period."
        
        response = f"🎯 **Goals - {name}**\n\n"
        response += "| Goal | Due Date | Status | Progress |\n"
        response += "|------|----------|--------|----------|\n"
        
        for goal in goals:
            status_emoji = "✅" if goal['status'] == 'completed' else ("🔄" if goal['status'] == 'in-progress' else "⏳")
            progress_bar = "█" * (goal['progress'] // 20) + "░" * (5 - goal['progress'] // 20)
            response += f"| {goal['title']} | {goal['due_date']} | {status_emoji} {goal['status'].title()} | {progress_bar} {goal['progress']}% |\n"
        
        return response
    
    def _get_kpis(self, employee_perf: Dict) -> str:
        """Get KPI metrics."""
        kpis = employee_perf.get('kpis', {})
        name = employee_perf['employee_name']
        
        if not kpis:
            return "📈 No KPI data available."
        
        response = f"📈 **KPI Metrics - {name}**\n\n"
        response += "| Metric | Score |\n"
        response += "|--------|-------|\n"
        
        for key, value in kpis.items():
            metric_name = key.replace('_', ' ').title()
            bar = "█" * (value // 20) + "░" * (5 - value // 20)
            response += f"| {metric_name} | {bar} {value}% |\n"
        
        return response
    
    def _get_feedback(self, employee_perf: Dict) -> str:
        """Get recent feedback."""
        feedback_list = employee_perf.get('recent_feedback', [])
        name = employee_perf['employee_name']
        
        if not feedback_list:
            return "💬 No recent feedback available."
        
        response = f"💬 **Recent Feedback - {name}**\n\n"
        
        for fb in feedback_list:
            type_emoji = "👏" if fb['type'] == 'praise' else ("🙏" if fb['type'] == 'thanks' else "💪")
            response += f"**{type_emoji} From {fb['from']}** ({fb['date']})\n"
            response += f"> {fb['message']}\n\n"
        
        return response
