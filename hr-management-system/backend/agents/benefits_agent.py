"""
Benefits Agent - Handles employee benefits queries with LLM enhancement.
"""
from typing import Dict, Optional
from . import BaseAgent, format_currency


class BenefitsAgent(BaseAgent):
    """Agent for handling benefits-related queries with LLM support."""
    
    KEYWORDS = [
        'benefit', 'insurance', 'health', 'medical', 'dental', 'vision',
        'retirement', '401k', '401(k)', 'pension', 'wellness', 'gym',
        'coverage', 'enroll', 'enrollment', 'life insurance'
    ]
    
    def __init__(self):
        super().__init__(
            name="Benefits Agent",
            description="Handles employee benefits and enrollment queries"
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
        benefits_data = self.load_json_data("benefits.json")
        
        packages = benefits_data.get('packages', {})
        enrollments = benefits_data.get('enrollments', {})
        employee_enrollment = enrollments.get(employee_id, None)
        
        # Try LLM response first
        if self.llm and self.llm.is_available():
            response = self.llm.generate_response(
                query=query,
                agent_name="Benefits Agent",
                context_data={
                    "available_packages": packages,
                    "employee_enrollment": employee_enrollment,
                    "enrollment_periods": benefits_data.get('enrollment_periods', {})
                },
                system_context="You are the Benefits Agent. Help employees understand their benefits, health insurance, 401k, and wellness programs. Present options clearly with costs and coverage details."
            )
            if response:
                return response
        
        # Fallback to rule-based response
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['my benefit', 'enrolled', 'my plan']):
            return self._get_enrolled_benefits(employee_enrollment, packages)
        elif any(word in query_lower for word in ['health', 'medical', 'dental']):
            return self._get_health_info(packages)
        elif any(word in query_lower for word in ['401k', '401(k)', 'retirement']):
            return self._get_retirement_info(packages, employee_enrollment)
        else:
            return self._get_benefits_summary(employee_enrollment, packages)
    
    def _get_enrolled_benefits(self, enrollment: Optional[Dict], packages: Dict) -> str:
        """Get employee's enrolled benefits."""
        if not enrollment:
            return "❌ No benefits enrollment found. Contact HR to enroll."
        
        response = f"🎁 **Your Benefits - {enrollment['employee_name']}**\n\n"
        
        for benefit in enrollment.get('enrolled_benefits', []):
            package = packages.get(benefit['package_id'], {})
            if package:
                response += f"### {package['name']}\n"
                response += f"- Status: {'✅ Active' if benefit['status'] == 'active' else '❌ Inactive'}\n"
                response += f"- Enrolled: {benefit['enrollment_date']}\n\n"
        
        return response
    
    def _get_health_info(self, packages: Dict) -> str:
        """Get health insurance information."""
        response = "🏥 **Health Insurance Plans**\n\n"
        
        for pkg_id, pkg in packages.items():
            if pkg.get('type') == 'health_insurance':
                response += f"### {pkg['name']}\n"
                response += f"- Monthly: {format_currency(pkg['monthly_cost'])} (You pay: {format_currency(pkg['employee_cost'])})\n"
                for cov_type, cov_desc in pkg.get('coverage', {}).items():
                    response += f"- {cov_type.title()}: {cov_desc}\n"
                response += "\n"
        
        return response
    
    def _get_retirement_info(self, packages: Dict, enrollment: Optional[Dict]) -> str:
        """Get retirement plan information."""
        retirement = packages.get('retirement_401k', {})
        
        contribution = None
        if enrollment:
            for b in enrollment.get('enrolled_benefits', []):
                if b['package_id'] == 'retirement_401k':
                    contribution = b.get('contribution_percent')
        
        response = f"""💰 **401(k) Retirement Plan**

- **Employer Match:** {retirement.get('employer_match', 'N/A')}
- **Vesting:** {retirement.get('vesting_schedule', 'N/A')}"""
        
        if contribution:
            response += f"\n- **Your Contribution:** {contribution}%"
        
        return response
    
    def _get_benefits_summary(self, enrollment: Optional[Dict], packages: Dict) -> str:
        """Get overall benefits summary."""
        if not enrollment:
            return """🎁 **Benefits Overview**

You don't have any benefits enrolled. Available:
- 🏥 Health Insurance
- 💰 401(k) Retirement
- 🛡️ Life Insurance
- 🏃 Wellness Program

Contact HR to enroll!"""
        
        count = len(enrollment.get('enrolled_benefits', []))
        return f"""🎁 **Benefits Summary - {enrollment['employee_name']}**

✅ Active Benefits: {count}

Ask me about:
- "My enrolled benefits"
- "Health insurance options"
- "401k details"
- "Wellness program\""""
