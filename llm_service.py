"""
Service for handling LLM interactions.
"""
import json
import requests
import time
import random
import re
from typing import Dict, Any, Optional
from enum import Enum
from config_loader import get_llm_config
from security_manager import security_manager, security_logger, sanitize_streamlit_output

class CircuitBreakerState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Circuit is open, rejecting requests
    HALF_OPEN = "half_open"  # Testing if service is back

class CircuitBreaker:
    """
    Circuit breaker pattern implementation for API calls.
    
    Prevents cascade failures by temporarily blocking requests
    when the service is experiencing high failure rates.
    """
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting to close circuit
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = CircuitBreakerState.CLOSED
    
    def can_execute(self) -> bool:
        """Check if request can be executed."""
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            return False
        else:  # HALF_OPEN
            return True
    
    def record_success(self):
        """Record a successful operation."""
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED
    
    def record_failure(self):
        """Record a failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

def retry_with_exponential_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator for retry logic with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for exponential backoff
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        # Exponential backoff with jitter
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        security_logger.warning(f"API call failed (attempt {attempt + 1}), retrying in {delay:.1f}s: {e}")
                        time.sleep(delay)
                    else:
                        security_logger.error(f"API call failed after {max_retries + 1} attempts: {e}")
            
            raise last_exception
        return wrapper
    return decorator

class PIIScrubber:
    """
    PII scrubbing service for GDPR/CCPA compliance
    
    Removes or masks personally identifiable information before
    sending data to external LLM services.
    """
    
    def __init__(self):
        """Initialize PII scrubber with patterns and replacements"""
        # Email patterns
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Phone number patterns (US, international)
        self.phone_patterns = [
            re.compile(r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'),
            re.compile(r'\b\+?[1-9]\d{1,14}\b'),  # International format
        ]
        
        # SSN patterns
        self.ssn_pattern = re.compile(r'\b\d{3}-?\d{2}-?\d{4}\b')
        
        # Credit card patterns (basic Luhn algorithm check)
        self.cc_pattern = re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b')
        
        # IP address patterns
        self.ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        
        # MAC address patterns
        self.mac_pattern = re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b')
        
        # Names that might be PII (common first/last name patterns)
        self.name_patterns = [
            re.compile(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'),  # First Last
        ]
        
        # Configure which fields to scrub
        self.scrub_config = {
            'emails': True,
            'phones': True,
            'ssns': True,
            'credit_cards': True,
            'ip_addresses': False,  # Might be needed for network analysis
            'mac_addresses': False,  # Might be needed for network analysis
            'names': False  # Too aggressive for business analysis
        }
    
    def scrub_text(self, text: str) -> str:
        """
        Scrub PII from text while preserving analytical value
        
        Args:
            text: Input text that may contain PII
            
        Returns:
            Scrubbed text with PII removed/masked
        """
        if not text or not isinstance(text, str):
            return text
        
        scrubbed = text
        
        # Email scrubbing
        if self.scrub_config.get('emails', True):
            scrubbed = self.email_pattern.sub('[EMAIL_REDACTED]', scrubbed)
        
        # Phone number scrubbing
        if self.scrub_config.get('phones', True):
            for pattern in self.phone_patterns:
                scrubbed = pattern.sub('[PHONE_REDACTED]', scrubbed)
        
        # SSN scrubbing
        if self.scrub_config.get('ssns', True):
            scrubbed = self.ssn_pattern.sub('[SSN_REDACTED]', scrubbed)
        
        # Credit card scrubbing
        if self.scrub_config.get('credit_cards', True):
            scrubbed = self.cc_pattern.sub('[CARD_REDACTED]', scrubbed)
        
        # IP address scrubbing (optional)
        if self.scrub_config.get('ip_addresses', False):
            scrubbed = self.ip_pattern.sub('[IP_REDACTED]', scrubbed)
        
        # MAC address scrubbing (optional)
        if self.scrub_config.get('mac_addresses', False):
            scrubbed = self.mac_pattern.sub('[MAC_REDACTED]', scrubbed)
        
        # Name scrubbing (optional - very aggressive)
        if self.scrub_config.get('names', False):
            for pattern in self.name_patterns:
                scrubbed = pattern.sub('[NAME_REDACTED]', scrubbed)
        
        return scrubbed
    
    def scrub_data_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively scrub PII from dictionary data
        
        Args:
            data: Dictionary that may contain PII in values
            
        Returns:
            Dictionary with PII scrubbed from string values
        """
        if not isinstance(data, dict):
            return data
        
        scrubbed_data = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                scrubbed_data[key] = self.scrub_text(value)
            elif isinstance(value, dict):
                scrubbed_data[key] = self.scrub_data_dict(value)
            elif isinstance(value, list):
                scrubbed_data[key] = [
                    self.scrub_text(item) if isinstance(item, str) 
                    else self.scrub_data_dict(item) if isinstance(item, dict)
                    else item
                    for item in value
                ]
            else:
                scrubbed_data[key] = value
        
        return scrubbed_data

class LLMService:
    def __init__(self) -> None:
        self.config: Dict[str, Any] = get_llm_config()
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)
        self.pii_scrubber = PIIScrubber()
        
    @retry_with_exponential_backoff(max_retries=3, base_delay=1.0)
    def _make_api_call(self, headers: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make the actual API call with timeout and error handling.
        
        Args:
            headers: HTTP headers for the request
            data: Request payload
            
        Returns:
            API response data
            
        Raises:
            requests.RequestException: If the API call fails
        """
        response = requests.post(
            f"{self.config['api_base']}/chat/completions",
            headers=headers,
            json=data,
            timeout=30  # 30-second timeout
        )
        
        if response.status_code != 200:
            error_msg = f"{response.status_code} - {response.text}"
            raise requests.RequestException(f"API call failed: {error_msg}")
        
        return response.json()

    def generate_insights(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Generate insights using the configured LLM with circuit breaker protection.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Dict containing structured insights or None if the call fails
        """
        # Check circuit breaker before attempting call
        if not self.circuit_breaker.can_execute():
            security_logger.warning("Circuit breaker is OPEN - rejecting LLM API request")
            return {
                "summary": "AI Insights temporarily unavailable due to service issues. Please try again later.",
                "key_insights": ["Service is experiencing connectivity issues", "Circuit breaker is active to prevent cascade failures"],
                "trends": ["Monitoring system health and API connectivity"],
                "recommended_actions": ["Please refresh the page in a few minutes", "Check network connectivity", "Contact support if the issue persists"]
            }
        
        try:
            # Validate and sanitize input (use ai_prompt type for relaxed validation)
            if not security_manager.validate_input(prompt, "ai_prompt"):
                security_logger.warning("Invalid prompt detected")
                return None
            
            # Scrub PII from prompt for GDPR/CCPA compliance
            scrubbed_prompt = self.pii_scrubber.scrub_text(prompt)
            if scrubbed_prompt != prompt:
                security_logger.info("PII detected and scrubbed from prompt for LLM compliance")
                prompt = scrubbed_prompt
            
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
            
            # Use the circuit breaker-protected API call
            response_data = self._make_api_call(headers, data)
            
            print(f"API Response: {response_data}")  # Debug log
            
            # Parse the JSON string from the LLM response
            content = response_data["choices"][0]["message"]["content"]
            
            try:
                insights = json.loads(content)
                
                # Basic validation of response structure
                required_keys = ["summary", "key_insights", "trends", "recommended_actions"]
                if not all(key in insights for key in required_keys):
                    security_logger.warning("Incomplete response structure from LLM")
                
                # Record success for circuit breaker
                self.circuit_breaker.record_success()
                
                # Return the insights directly (structured data doesn't need text sanitization)
                return insights
                
            except json.JSONDecodeError as e:
                security_logger.error(f"Failed to parse LLM response as JSON: {e}")
                self.circuit_breaker.record_failure()
                return None
            
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
            
            # Record failure for circuit breaker
            self.circuit_breaker.record_failure()
            
            return {
                "summary": "AI Insights temporarily unavailable due to technical issues. Please try again later.",
                "key_insights": ["Service is experiencing technical difficulties"],
                "trends": ["Monitoring service health and performance"],
                "recommended_actions": ["Please refresh the page and try again", "Contact support if the issue persists"]
            }

    def format_insights_for_display(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw insights into a structure suitable for display.
        
        Args:
            insights: Raw insights from LLM
            
        Returns:
            Dict containing formatted insights with HTML/markdown formatting
        """
        if not insights or not isinstance(insights, dict):
            return {
                "summary": "⚠️ Unable to generate insights at this time.",
                "key_insights": [],
                "trends": [],
                "recommended_actions": []
            }
        
        # Validate required keys are present
        required_keys = ['summary', 'key_insights', 'trends', 'recommended_actions']
        if not all(key in insights for key in required_keys):
            return {
                "summary": "⚠️ Insights format is incomplete.",
                "key_insights": [],
                "trends": [],
                "recommended_actions": []
            }
            
        # Add emoji indicators and formatting, with safe defaults and text sanitization
        try:
            from security_manager import sanitize_streamlit_output
            
            formatted = {
                "summary": f"📊 {sanitize_streamlit_output(insights.get('summary', 'No summary available'))}",
                "key_insights": [f"💡 {sanitize_streamlit_output(insight)}" for insight in insights.get('key_insights', []) if isinstance(insight, str)],
                "trends": [f"📈 {sanitize_streamlit_output(trend)}" for trend in insights.get('trends', []) if isinstance(trend, str)],
                "recommended_actions": [f"✅ {sanitize_streamlit_output(action)}" for action in insights.get('recommended_actions', []) if isinstance(action, str)]
            }
            
            return formatted
        except Exception as e:
            security_logger.error(f"Error formatting insights for display: {e}")
            return {
                "summary": "⚠️ Error formatting insights.",
                "key_insights": [],
                "trends": [],
                "recommended_actions": []
            }