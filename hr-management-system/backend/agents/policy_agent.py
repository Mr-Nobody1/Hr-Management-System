"""
Policy Agent - Handles HR policy and FAQ queries with LLM enhancement.
"""
from typing import Dict, Optional, List
from . import BaseAgent


class PolicyAgent(BaseAgent):
    """Agent for handling policy and FAQ queries with LLM support."""
    
    KEYWORDS = [
        'policy', 'policies', 'rule', 'rules', 'guideline', 'guidelines',
        'wfh', 'work from home', 'remote', 'dress code', 'dress',
        'expense', 'reimbursement', 'conduct', 'behavior', 'faq',
        'how do i', 'what is the', 'allowed', 'permitted', 'can i'
    ]
    
    def __init__(self):
        super().__init__(
            name="Policy Agent",
            description="Handles HR policies, guidelines, and FAQ queries"
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
        policies_data = self.load_json_data("policies.json")
        
        # Try LLM response first
        if self.llm and self.llm.is_available():
            # Find relevant policies based on query
            relevant_policies = self._find_relevant_policies(query, policies_data)
            relevant_faqs = self._find_relevant_faqs(query, policies_data)
            
            response = self.llm.generate_response(
                query=query,
                agent_name="Policy Agent",
                context_data={
                    "relevant_policies": relevant_policies,
                    "relevant_faqs": relevant_faqs,
                    "all_policy_categories": list(set(p['category'] for p in policies_data.get('policies', [])))
                },
                system_context="You are the Policy Agent. Help employees understand HR policies, company guidelines, and answer common questions. Be clear and cite specific policies when applicable. If a policy doesn't exist for what they're asking, suggest they contact HR directly."
            )
            if response:
                return response
        
        # Fallback to rule-based response
        query_lower = query.lower()
        
        # Check for specific policy categories
        if any(word in query_lower for word in ['wfh', 'work from home', 'remote', 'hybrid']):
            return self._get_policy_by_id('POL001', policies_data)
        elif any(word in query_lower for word in ['dress', 'attire', 'clothing']):
            return self._get_policy_by_id('POL002', policies_data)
        elif any(word in query_lower for word in ['leave', 'vacation', 'pto', 'time off']):
            return self._get_policy_by_id('POL003', policies_data)
        elif any(word in query_lower for word in ['expense', 'reimbursement', 'travel']):
            return self._get_policy_by_id('POL004', policies_data)
        elif any(word in query_lower for word in ['conduct', 'behavior', 'ethics', 'harassment']):
            return self._get_policy_by_id('POL005', policies_data)
        else:
            return self._get_all_policies_summary(policies_data)
    
    def _find_relevant_policies(self, query: str, policies_data: Dict) -> List[Dict]:
        """Find policies relevant to the query."""
        query_lower = query.lower()
        relevant = []
        
        for policy in policies_data.get('policies', []):
            # Check keywords
            keywords = policy.get('keywords', [])
            if any(kw in query_lower for kw in keywords):
                relevant.append(policy)
            # Check title and category
            elif policy['title'].lower() in query_lower or policy['category'].lower() in query_lower:
                relevant.append(policy)
        
        return relevant[:3]  # Return top 3 relevant policies
    
    def _find_relevant_faqs(self, query: str, policies_data: Dict) -> List[Dict]:
        """Find FAQs relevant to the query."""
        query_lower = query.lower()
        relevant = []
        
        for faq in policies_data.get('faqs', []):
            if any(word in faq['question'].lower() for word in query_lower.split()):
                relevant.append(faq)
        
        return relevant[:3]  # Return top 3 relevant FAQs
    
    def _get_policy_by_id(self, policy_id: str, policies_data: Dict) -> str:
        """Get a specific policy by ID."""
        for policy in policies_data.get('policies', []):
            if policy['id'] == policy_id:
                return f"""📋 **{policy['title']}**

**Category:** {policy['category']}
**Effective:** {policy['effective_date']} | **Updated:** {policy['last_updated']}

---

### Summary
{policy['summary']}

### Details
{policy['content']}

---
💡 *For clarification, contact HR at hr@company.com*"""
        
        return "❌ Policy not found."
    
    def _get_all_policies_summary(self, policies_data: Dict) -> str:
        """Get a summary of all available policies."""
        policies = policies_data.get('policies', [])
        
        response = """📚 **Company Policies**

| Category | Policy | Summary |
|----------|--------|---------|
"""
        
        for policy in policies:
            response += f"| {policy['category']} | {policy['title']} | {policy['summary'][:50]}... |\n"
        
        response += """

---

### 💬 Common Questions

"""
        
        for faq in policies_data.get('faqs', [])[:3]:
            response += f"**Q: {faq['question']}**\n> {faq['answer']}\n\n"
        
        response += """
💡 *Ask me about any specific policy for more details!*"""
        
        return response
