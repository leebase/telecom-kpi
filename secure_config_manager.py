"""
Advanced Secure Configuration Manager
Supports multiple secure configuration sources with fallback hierarchy
"""

import os
import yaml
import base64
import json
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from security_manager import security_logger

class SecureConfigManager:
    """Advanced configuration manager with multiple security layers"""
    
    def __init__(self):
        self.config_sources = [
            self._load_from_environment,
            self._load_from_encrypted_file,
            self._load_from_secure_file,
            self._load_from_template
        ]
        
    def get_config(self) -> Dict[str, Any]:
        """Load configuration from the most secure available source"""
        for source in self.config_sources:
            try:
                config = source()
                if config and self._validate_config(config):
                    source_name = source.__name__.replace('_load_from_', '')
                    security_logger.info(f"Configuration loaded from: {source_name}")
                    return config
            except Exception as e:
                security_logger.debug(f"Config source {source.__name__} failed: {e}")
                continue
        
        security_logger.error("No valid configuration source found")
        return self._get_minimal_config()
    
    def _load_from_environment(self) -> Optional[Dict[str, Any]]:
        """Load from environment variables (highest priority)"""
        api_key = os.getenv('LLM_API_KEY')
        if not api_key:
            return None
            
        return {
            'llm': {
                'provider': os.getenv('LLM_PROVIDER', 'openrouter'),
                'api_key': api_key,
                'model': os.getenv('LLM_MODEL', 'openai/gpt-4-1106-preview'),
                'temperature': float(os.getenv('LLM_TEMPERATURE', '0.7')),
                'max_tokens': int(os.getenv('LLM_MAX_TOKENS', '1000')),
                'api_base': os.getenv('LLM_API_BASE', 'https://openrouter.ai/api/v1')
            }
        }
    
    def _load_from_encrypted_file(self) -> Optional[Dict[str, Any]]:
        """Load from encrypted configuration file"""
        encrypted_path = Path('config.secrets.enc')
        key_path = Path('.encryption_key')
        
        if not (encrypted_path.exists() and key_path.exists()):
            return None
        
        try:
            # Load encryption key
            with open(key_path, 'rb') as f:
                key = f.read()
            
            # Decrypt configuration
            fernet = Fernet(key)
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = fernet.decrypt(encrypted_data)
            config = yaml.safe_load(decrypted_data.decode())
            
            security_logger.info("Configuration loaded from encrypted file")
            return config
            
        except Exception as e:
            security_logger.error(f"Failed to decrypt configuration: {e}")
            return None
    
    def _load_from_secure_file(self) -> Optional[Dict[str, Any]]:
        """Load from secure file with permission checks"""
        config_path = Path('config.secrets.yaml')
        
        if not config_path.exists():
            return None
        
        # Check file permissions (Unix-like systems)
        if hasattr(os, 'stat'):
            stat_info = config_path.stat()
            # Check if file is readable by others (should be 600 or 640 max)
            if stat_info.st_mode & 0o044:  # Check if group/other can read
                security_logger.warning("Config file has overly permissive permissions")
                return None
        
        try:
            with open(config_path, 'r') as f:
                content = f.read()
            
            # Substitute environment variables if present
            content = self._substitute_env_vars(content)
            config = yaml.safe_load(content)
            
            return config
            
        except Exception as e:
            security_logger.error(f"Failed to load secure file: {e}")
            return None
    
    def _load_from_template(self) -> Optional[Dict[str, Any]]:
        """Load from template file (development fallback)"""
        template_path = Path('config.template.yaml')
        
        if not template_path.exists():
            return None
        
        try:
            with open(template_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Only use if API key is not a placeholder
            api_key = config.get('llm', {}).get('api_key', '')
            if api_key and not api_key.startswith('your-') and not api_key.startswith('REPLACE'):
                return config
            
            return None
            
        except Exception as e:
            security_logger.error(f"Failed to load template: {e}")
            return None
    
    def _substitute_env_vars(self, content: str) -> str:
        """Substitute environment variables in configuration content"""
        import re
        
        def replace_env_var(match):
            var_name = match.group(1)
            default_value = match.group(2) if len(match.groups()) > 1 else None
            env_value = os.getenv(var_name, default_value)
            
            if env_value is None:
                security_logger.warning(f"Environment variable {var_name} not found")
                return ""
            
            return env_value
        
        # Replace ${VAR_NAME} and ${VAR_NAME:-default} patterns
        content = re.sub(r'\$\{([^}:]+)(?::-([^}]*))?\}', replace_env_var, content)
        return content
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration for security and completeness"""
        try:
            llm_config = config.get('llm', {})
            api_key = llm_config.get('api_key', '')
            
            # API key should exist and not be a placeholder
            if not api_key or api_key.startswith('your-') or api_key.startswith('REPLACE'):
                return False
            
            # Validate required fields
            required_fields = ['provider', 'api_key', 'model']
            for field in required_fields:
                if not llm_config.get(field):
                    return False
            
            return True
            
        except Exception as e:
            security_logger.error(f"Configuration validation error: {e}")
            return False
    
    def _get_minimal_config(self) -> Dict[str, Any]:
        """Return minimal configuration for graceful degradation"""
        return {
            'llm': {
                'provider': 'openrouter',
                'api_key': None,  # Will disable AI features
                'model': 'openai/gpt-4-1106-preview',
                'temperature': 0.7,
                'max_tokens': 1000,
                'api_base': 'https://openrouter.ai/api/v1'
            }
        }
    
    def encrypt_config(self, config_file: str = 'config.secrets.yaml') -> bool:
        """Encrypt an existing configuration file"""
        try:
            config_path = Path(config_file)
            if not config_path.exists():
                security_logger.error(f"Configuration file {config_file} not found")
                return False
            
            # Generate encryption key
            key = Fernet.generate_key()
            fernet = Fernet(key)
            
            # Read and encrypt configuration
            with open(config_path, 'rb') as f:
                data = f.read()
            
            encrypted_data = fernet.encrypt(data)
            
            # Save encrypted file and key
            with open('config.secrets.enc', 'wb') as f:
                f.write(encrypted_data)
            
            with open('.encryption_key', 'wb') as f:
                f.write(key)
            
            # Secure the key file
            os.chmod('.encryption_key', 0o600)
            os.chmod('config.secrets.enc', 0o600)
            
            security_logger.info("Configuration encrypted successfully")
            print("✅ Configuration encrypted. Keep .encryption_key secure!")
            return True
            
        except Exception as e:
            security_logger.error(f"Failed to encrypt configuration: {e}")
            return False

# Global secure config manager
secure_config = SecureConfigManager()
