"""
Payslip Agent - Handles salary and payslip queries with LLM enhancement.
"""
from typing import Dict, Optional
from . import BaseAgent, format_currency


class PayslipAgent(BaseAgent):
    """Agent for handling payslip and salary-related queries with LLM support."""
    
    KEYWORDS = [
        'payslip', 'salary', 'pay', 'payment', 'wage', 'income',
        'deduction', 'tax', 'gross', 'net', 'earnings', 'compensation',
        'how much', 'money', 'paid'
    ]
    
    def __init__(self):
        super().__init__(
            name="Payslip Agent",
            description="Handles payslip generation and salary queries"
        )
        # Try to import LLM service
        try:
            from llm_service import llm_service
            self.llm = llm_service
        except ImportError:
            self.llm = None
    
    def can_handle(self, query: str) -> bool:
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.KEYWORDS)
    
    def process(self, query: str, employee_id: str, context: Optional[Dict] = None) -> str:
        payslips_data = self.load_json_data("payslips.json")
        
        if employee_id not in payslips_data:
            return "❌ Sorry, I couldn't find your payslip records."
        
        employee_payslips = payslips_data[employee_id]
        
        # Try LLM response first
        if self.llm and self.llm.is_available():
            response = self.llm.generate_response(
                query=query,
                agent_name="Payslip Agent",
                context_data={
                    "employee_name": employee_payslips.get("employee_name"),
                    "employee_id": employee_id,
                    "payslips": employee_payslips.get("payslips", [])
                },
                system_context="You are the Payslip Agent. Help employees understand their salary, payslips, deductions, and taxes. Present payslip data in clear tables with proper currency formatting."
            )
            if response:
                return response
        
        # Fallback to rule-based response
        query_lower = query.lower()
        payslips = employee_payslips.get('payslips', [])
        
        if not payslips:
            return "❌ No payslips found for your account."
        
        if any(word in query_lower for word in ['history', 'all', 'previous', 'past']):
            return self._get_payslip_history(employee_payslips)
        elif any(word in query_lower for word in ['deduction', 'tax']):
            return self._get_deductions(payslips[0], employee_payslips['employee_name'])
        else:
            return self._get_current_payslip(payslips[0], employee_payslips['employee_name'])
    
    def _get_current_payslip(self, payslip: Dict, employee_name: str) -> str:
        """Get the current/latest payslip."""
        allowances = payslip['allowances']
        deductions = payslip['deductions']
        
        return f"""💰 **Payslip - {payslip['month']} {payslip['year']}**

**Employee:** {employee_name}  
**Pay Period:** {payslip['pay_period']}  
**Payment Date:** {payslip['payment_date']}

---

### 📈 Earnings

| Description | Amount |
|-------------|--------|
| Basic Salary | {format_currency(payslip['basic_salary'])} |
| Housing Allowance | {format_currency(allowances['housing'])} |
| Transport Allowance | {format_currency(allowances['transport'])} |
| Meal Allowance | {format_currency(allowances['meal'])} |
| **Gross Salary** | **{format_currency(payslip['gross_salary'])}** |

---

### 📉 Deductions

| Description | Amount |
|-------------|--------|
| Federal Tax | {format_currency(deductions['federal_tax'])} |
| State Tax | {format_currency(deductions['state_tax'])} |
| Social Security | {format_currency(deductions['social_security'])} |
| Medicare | {format_currency(deductions['medicare'])} |
| Health Insurance | {format_currency(deductions['health_insurance'])} |
| 401(k) | {format_currency(deductions['retirement_401k'])} |
| **Total Deductions** | **{format_currency(payslip['total_deductions'])}** |

---

### 💵 Net Pay: **{format_currency(payslip['net_salary'])}**"""
    
    def _get_payslip_history(self, employee_data: Dict) -> str:
        """Get payslip history."""
        payslips = employee_data.get('payslips', [])
        
        response = f"📋 **Payslip History for {employee_data['employee_name']}**\n\n"
        response += "| Month | Year | Gross | Net | Date |\n"
        response += "|-------|------|-------|-----|------|\n"
        
        for payslip in payslips:
            response += f"| {payslip['month']} | {payslip['year']} | {format_currency(payslip['gross_salary'])} | {format_currency(payslip['net_salary'])} | {payslip['payment_date']} |\n"
        
        return response
    
    def _get_deductions(self, payslip: Dict, employee_name: str) -> str:
        """Get detailed deduction breakdown."""
        deductions = payslip['deductions']
        total = payslip['total_deductions']
        gross = payslip['gross_salary']
        
        response = f"📊 **Deduction Breakdown - {payslip['month']} {payslip['year']}**\n\n"
        response += "| Category | Amount | % of Gross |\n"
        response += "|----------|--------|------------|\n"
        
        for name, amount in deductions.items():
            display_name = name.replace('_', ' ').title()
            percentage = (amount / gross) * 100
            response += f"| {display_name} | {format_currency(amount)} | {percentage:.1f}% |\n"
        
        response += f"| **Total** | **{format_currency(total)}** | **{(total/gross)*100:.1f}%** |\n"
        response += f"\n💵 Take-home: **{(1 - total/gross)*100:.1f}%** of gross"
        
        return response
