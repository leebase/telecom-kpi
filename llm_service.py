"""
Service for handling LLM interactions.
"""
import json
import requests
from typing import Dict, Any, Optional
from config_loader import get_llm_config
from security_manager import security_manager, security_logger, sanitize_streamlit_output

class LLMService:
    def __init__(self):
        self.config = get_llm_config()
        
    def generate_insights(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Generate insights using the configured LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Dict containing structured insights or None if the call fails
        """
        try:
            # Validate and sanitize input
            if not security_manager.validate_input(prompt):
                security_logger.warning("Invalid prompt detected")
                return None
            
            # Rate limiting check
            if not security_manager.rate_limit_check("llm_api"):
                security_logger.warning("Rate limit exceeded for LLM API")
                return None
            headers = {
                "Authorization": f"Bearer {self.config['api_key']}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-repo/telecomdashboard",  # Required by OpenRouter
            }
            
            data = {
                "model": self.config["model"],
                "messages": [
                    {
                        "role": "system",
                        "content": """You are an expert telecommunications analyst AI. Analyze the KPI data and provide clear, actionable insights.
                        Focus on identifying patterns, anomalies, and suggesting specific corrective actions.
                        
                        Format your response as a JSON object with this structure:
                        {
                            "summary": "One paragraph overview of key findings",
                            "key_insights": ["3-5 important observations"],
                            "trends": ["2-3 significant trends"],
                            "recommended_actions": ["3-5 specific, actionable recommendations"]
                        }
                        
                        Make your insights specific, data-driven, and actionable. Focus on business impact and clear next steps."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": self.config.get("temperature", 0.7),
                "max_tokens": self.config.get("max_tokens", 1000),
                "response_format": { "type": "json_object" }
            }
            
            print(f"Making API call to {self.config['api_base']}/chat/completions")  # Debug log
            response = requests.post(
                f"{self.config['api_base']}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Error from LLM API: {response.status_code} - {response.text}")
                return None
                
            result = response.json()
            print(f"API Response: {result}")  # Debug log
            
            # Parse the JSON string from the LLM response
            content = result["choices"][0]["message"]["content"]
            insights = json.loads(content)
            return insights
            
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return None

    def format_insights_for_display(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw insights into a structure suitable for display.
        
        Args:
            insights: Raw insights from LLM
            
        Returns:
            Dict containing formatted insights with HTML/markdown formatting
        """
        if not insights:
            return {
                "summary": "⚠️ Unable to generate insights at this time.",
                "key_insights": [],
                "trends": [],
                "recommended_actions": []
            }
            
        # Add emoji indicators and formatting
        formatted = {
            "summary": f"📊 {insights['summary']}",
            "key_insights": [f"💡 {insight}" for insight in insights.get('key_insights', [])],
            "trends": [f"📈 {trend}" for trend in insights.get('trends', [])],
            "recommended_actions": [f"✅ {action}" for action in insights.get('recommended_actions', [])]
        }
        
        return formatted