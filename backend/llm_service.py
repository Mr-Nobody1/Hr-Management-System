"""
LLM Service - Google Gemini integration for the HR Management System.
Provides intelligent routing and natural language responses using gemini-2.5-flash.
"""
import os
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class LLMService:
    """Service for LLM-powered HR assistant functionality using Gemini 2.5 Flash."""
    
    def __init__(self):
        self.model_name = "gemini-2.5-flash"
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Gemini model if API key is available."""
        if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                self.model = genai.GenerativeModel(self.model_name)
                print(f"✅ Gemini LLM initialized with model: {self.model_name}")
            except Exception as e:
                print(f"❌ Failed to initialize Gemini: {e}")
                self.model = None
        else:
            print("⚠️ Gemini API key not configured. Using fallback keyword-based mode.")
            self.model = None
    
    def is_available(self) -> bool:
        """Check if LLM service is available."""
        return self.model is not None
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """
        Use LLM to intelligently route the query to the appropriate agent.
        Returns: {"agent": "agent_name", "intent": "detected_intent", "confidence": 0.0-1.0}
        """
        if not self.is_available():
            return {"agent": None, "intent": None, "confidence": 0.0}
        
        routing_prompt = f"""You are an HR assistant router. Analyze the user's query and determine which specialized agent should handle it.

Available agents:
1. PAYSLIP - Handles salary, payslips, pay, income, deductions, tax, earnings, compensation, money earned
2. LEAVE - Handles vacation, time off, PTO, sick leave, annual leave, personal leave, absence, leave balance, holiday requests
3. EMPLOYEE - Handles employee profile, team members, department info, manager info, coworkers, personal details, "who am I"
4. ATTENDANCE - Handles clock in/out, check in/out, work hours, overtime, attendance records, schedule, punctuality, late arrivals
5. BENEFITS - Handles health insurance, 401k, retirement, dental, vision, wellness programs, benefits enrollment, medical coverage
6. PERFORMANCE - Handles performance reviews, ratings, goals, KPIs, feedback, evaluations, appraisals, objectives
7. POLICY - Handles HR policies, company rules, guidelines, WFH policy, dress code, FAQs, code of conduct
8. GENERAL - For greetings (hello, hi), help requests, and general HR questions that don't fit specific categories

User query: "{query}"

Respond ONLY with a valid JSON object in this exact format (no markdown, no explanation):
{{"agent": "AGENT_NAME", "intent": "brief description of what user wants", "confidence": 0.95}}

Choose the most appropriate agent based on the user's intent. Use GENERAL only for greetings or if truly uncertain."""

        try:
            response = self.model.generate_content(routing_prompt)
            response_text = response.text.strip()
            
            # Clean up the response (remove markdown code blocks if present)
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
            response_text = response_text.strip()
            
            result = json.loads(response_text)
            return result
        except Exception as e:
            print(f"Routing error: {e}")
            return {"agent": "GENERAL", "intent": "unknown", "confidence": 0.5}
    
    def generate_response(
        self, 
        query: str, 
        agent_name: str,
        context_data: Dict[str, Any],
        system_context: str = "",
        language: str = "en",
        conversation_history: str = ""
    ) -> str:
        """
        Generate an intelligent response using the LLM.
        
        Args:
            query: User's question
            agent_name: Which agent is responding
            context_data: Relevant data to include (e.g., payslip data, leave balance)
            system_context: Additional context about the agent's role
            language: Language code for response
            conversation_history: Previous conversation context
        """
        if not self.is_available():
            return None
        
        # Get language instruction
        try:
            from translations import get_language_instruction
            language_instruction = get_language_instruction(language)
        except ImportError:
            language_instruction = ""
        
        # Build conversation context
        history_context = f"\n{conversation_history}\n" if conversation_history else ""
        
        prompt = f"""{system_context}

You are the {agent_name} for an HR Management System. Generate a helpful, friendly response to the user's query.
{language_instruction}
Important guidelines:
- Use markdown formatting for better readability
- Use tables when presenting structured data
- Use emojis sparingly to make responses engaging
- Be concise but thorough
- Format currency values properly (e.g., $1,234.56)
- Format dates in a readable way (e.g., December 5, 2024)
- If data is available, present it clearly
- If data is not available for what they asked, explain what IS available
- Consider the conversation history for context when answering follow-up questions
{history_context}
User Query: "{query}"

Available Data:
{json.dumps(context_data, indent=2, default=str)}

Generate a natural, helpful response based on this data:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Response generation error: {e}")
            return None


# Singleton instance
llm_service = LLMService()
