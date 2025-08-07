"""
Configuration loader for API keys and other sensitive data.
"""
import os
import yaml
from typing import Dict, Any, Optional

def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.secrets.yaml.
    Falls back to environment variables if file not found.
    
    Returns:
        Dict containing configuration values
    """
    # Try to load from config file
    config_path = os.path.join(os.path.dirname(__file__), 'config.secrets.yaml')
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    # Fall back to environment variables
    return {
        'llm': {
            'provider': os.getenv('LLM_PROVIDER', 'openrouter'),
            'api_key': os.getenv('LLM_API_KEY'),
            'model': os.getenv('LLM_MODEL', 'mistral-7b-instruct'),
            'temperature': float(os.getenv('LLM_TEMPERATURE', '0.7')),
            'max_tokens': int(os.getenv('LLM_MAX_TOKENS', '1000')),
            'api_base': os.getenv('LLM_API_BASE', 'https://openrouter.ai/api/v1')
        }
    }

def get_llm_config() -> Dict[str, Any]:
    """
    Get LLM-specific configuration.
    
    Returns:
        Dict containing LLM configuration
    """
    config = load_config()
    return config.get('llm', {})

def get_api_key() -> Optional[str]:
    """
    Get the API key for the LLM provider.
    
    Returns:
        API key string or None if not found
    """
    return get_llm_config().get('api_key')
