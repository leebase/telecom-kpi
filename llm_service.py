"""
Service for handling LLM interactions.
"""
import json
import requests
from typing import Dict, Any, Optional
from config_loader import get_llm_config
from security_manager import security_manager, security_logger, sanitize_streamlit_output

class LLMService:
    def __init__(self) -> None:
        self.config: Dict[str, Any] = get_llm_config()
        
    def generate_insights(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Generate insights using the configured LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Dict containing structured insights or None if the call fails
        """
        try:
            # Validate and sanitize input (use ai_prompt type for relaxed validation)
            if not security_manager.validate_input(prompt, "ai_prompt"):
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
                error_msg = f"Error from LLM API: {response.status_code} - {response.text}"
                print(error_msg)
                
                # Return helpful error message for common issues
                if response.status_code == 401:
                    return {
                        "error": "API Authentication Failed",
                        "summary": "⚠️ OpenRouter API key is invalid or expired. Please get a new API key from https://openrouter.ai/",
                        "key_insights": [
                            "The API key provided is not recognized by OpenRouter",
                            "This could be due to an expired key or incorrect key format",
                            "OpenRouter requires a valid account with sufficient credits"
                        ],
                        "trends": [
                            "Authentication errors prevent AI analysis from functioning"
                        ],
                        "recommended_actions": [
                            "Visit https://openrouter.ai/ to get a new API key",
                            "Check your OpenRouter account status and billing",
                            "Verify the API key is correctly set in environment variables",
                            "Ensure your account has sufficient credits for API calls"
                        ]
                    }
                return None
                
            result = response.json()
            print(f"API Response: {result}")  # Debug log
            
            # Parse the JSON string from the LLM response
            content = result["choices"][0]["message"]["content"]
            insights = json.loads(content)
            return insights
            
        except requests.exceptions.ConnectionError as e:
            security_logger.error(f"LLM API connection error: {e}")
            return {"error": "Connection failed", "summary": "Unable to connect to AI service"}
        except requests.exceptions.Timeout as e:
            security_logger.error(f"LLM API timeout: {e}")
            return {"error": "Request timeout", "summary": "AI service request timed out"}
        except requests.exceptions.RequestException as e:
            security_logger.error(f"LLM API request error: {e}")
            return {"error": "Request failed", "summary": "AI service request failed"}
        except json.JSONDecodeError as e:
            security_logger.error(f"LLM response JSON parsing error: {e}")
            return {"error": "Invalid response", "summary": "AI service returned invalid data"}
        except KeyError as e:
            security_logger.error(f"LLM response missing expected key: {e}")
            return {"error": "Malformed response", "summary": "AI service response incomplete"}
        except Exception as e:
            security_logger.error(f"Unexpected LLM service error: {e}")
            return {"error": "Service error", "summary": "Unexpected AI service error"}

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