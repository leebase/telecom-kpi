"""
Centralized Configuration Management System

This module provides a unified interface for managing application configuration,
including database settings, UI preferences, security settings, and performance tuning.
"""

import os
import yaml
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    path: str = "data/telecom_db.sqlite"
    connection_timeout: int = 30000
    enable_foreign_keys: bool = True
    cache_size: int = 32
    trend_cache_size: int = 16

@dataclass
class UIConfig:
    """User interface configuration settings"""
    default_theme: str = "verizon"
    page_title: str = "Telecom KPI Dashboard"
    page_icon: str = "📡"
    layout: str = "wide"
    sidebar_state: str = "expanded"
    show_debug_info: bool = False

@dataclass
class SecurityConfig:
    """Security configuration settings"""
    enable_rate_limiting: bool = True
    max_requests_per_minute: int = 60
    enable_input_validation: bool = True
    enable_output_sanitization: bool = True
    enable_security_logging: bool = True
    log_file: str = "security.log"

@dataclass
class PerformanceConfig:
    """Performance optimization settings"""
    enable_caching: bool = True
    cache_ttl_seconds: int = 300
    max_dataframe_rows: int = 10000
    enable_lazy_loading: bool = True
    concurrent_requests: int = 5

@dataclass
class AIConfig:
    """AI/LLM configuration settings"""
    model: str = "openai/gpt-4-1106-preview"
    temperature: float = 0.1
    max_tokens: int = 2000
    api_timeout: int = 30
    enable_insights: bool = True

@dataclass
class AppConfig:
    """Main application configuration"""
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate configuration values"""
        if self.database.cache_size < 1:
            raise ValueError("Database cache size must be at least 1")
        
        if self.performance.cache_ttl_seconds < 0:
            raise ValueError("Cache TTL cannot be negative")
        
        if self.ai.temperature < 0 or self.ai.temperature > 2:
            raise ValueError("AI temperature must be between 0 and 2")
        
        if self.performance.max_dataframe_rows < 100:
            raise ValueError("Max dataframe rows must be at least 100")

class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or "config.yaml"
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        self._config: Optional[AppConfig] = None
        
    @property
    def config(self) -> AppConfig:
        """Get current configuration, loading if necessary"""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def load_config(self) -> AppConfig:
        """Load configuration from file or create default"""
        config_path = self.config_dir / self.config_file
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
                return self._create_config_from_dict(config_data)
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
                logger.info("Using default configuration")
        
        # Return default configuration
        return AppConfig()
    
    def save_config(self, config: Optional[AppConfig] = None) -> None:
        """Save configuration to file"""
        config = config or self.config
        config_path = self.config_dir / self.config_file
        
        try:
            config_dict = self._config_to_dict(config)
            with open(config_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
            logger.info(f"Configuration saved to {config_path}")
        except Exception as e:
            logger.error(f"Failed to save config to {config_path}: {e}")
    
    def _create_config_from_dict(self, config_data: Dict[str, Any]) -> AppConfig:
        """Create AppConfig from dictionary"""
        config = AppConfig()
        
        # Update database config
        if 'database' in config_data:
            db_config = config_data['database']
            for key, value in db_config.items():
                if hasattr(config.database, key):
                    setattr(config.database, key, value)
        
        # Update UI config
        if 'ui' in config_data:
            ui_config = config_data['ui']
            for key, value in ui_config.items():
                if hasattr(config.ui, key):
                    setattr(config.ui, key, value)
        
        # Update security config
        if 'security' in config_data:
            security_config = config_data['security']
            for key, value in security_config.items():
                if hasattr(config.security, key):
                    setattr(config.security, key, value)
        
        # Update performance config
        if 'performance' in config_data:
            perf_config = config_data['performance']
            for key, value in perf_config.items():
                if hasattr(config.performance, key):
                    setattr(config.performance, key, value)
        
        # Update AI config
        if 'ai' in config_data:
            ai_config = config_data['ai']
            for key, value in ai_config.items():
                if hasattr(config.ai, key):
                    setattr(config.ai, key, value)
        
        return config
    
    def _config_to_dict(self, config: AppConfig) -> Dict[str, Any]:
        """Convert AppConfig to dictionary"""
        return {
            'database': {
                'path': config.database.path,
                'connection_timeout': config.database.connection_timeout,
                'enable_foreign_keys': config.database.enable_foreign_keys,
                'cache_size': config.database.cache_size,
                'trend_cache_size': config.database.trend_cache_size,
            },
            'ui': {
                'default_theme': config.ui.default_theme,
                'page_title': config.ui.page_title,
                'page_icon': config.ui.page_icon,
                'layout': config.ui.layout,
                'sidebar_state': config.ui.sidebar_state,
                'show_debug_info': config.ui.show_debug_info,
            },
            'security': {
                'enable_rate_limiting': config.security.enable_rate_limiting,
                'max_requests_per_minute': config.security.max_requests_per_minute,
                'enable_input_validation': config.security.enable_input_validation,
                'enable_output_sanitization': config.security.enable_output_sanitization,
                'enable_security_logging': config.security.enable_security_logging,
                'log_file': config.security.log_file,
            },
            'performance': {
                'enable_caching': config.performance.enable_caching,
                'cache_ttl_seconds': config.performance.cache_ttl_seconds,
                'max_dataframe_rows': config.performance.max_dataframe_rows,
                'enable_lazy_loading': config.performance.enable_lazy_loading,
                'concurrent_requests': config.performance.concurrent_requests,
            },
            'ai': {
                'model': config.ai.model,
                'temperature': config.ai.temperature,
                'max_tokens': config.ai.max_tokens,
                'api_timeout': config.ai.api_timeout,
                'enable_insights': config.ai.enable_insights,
            }
        }
    
    def get_database_config(self) -> DatabaseConfig:
        """Get database configuration"""
        return self.config.database
    
    def get_ui_config(self) -> UIConfig:
        """Get UI configuration"""
        return self.config.ui
    
    def get_security_config(self) -> SecurityConfig:
        """Get security configuration"""
        return self.config.security
    
    def get_performance_config(self) -> PerformanceConfig:
        """Get performance configuration"""
        return self.config.performance
    
    def get_ai_config(self) -> AIConfig:
        """Get AI configuration"""
        return self.config.ai
    
    def update_config(self, **kwargs) -> None:
        """Update configuration values"""
        config = self.config
        
        for section, values in kwargs.items():
            if hasattr(config, section):
                section_config = getattr(config, section)
                for key, value in values.items():
                    if hasattr(section_config, key):
                        setattr(section_config, key, value)
                    else:
                        logger.warning(f"Unknown config key: {section}.{key}")
            else:
                logger.warning(f"Unknown config section: {section}")
        
        # Re-validate after updates
        config._validate_config()
        self.save_config(config)
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults"""
        self._config = AppConfig()
        self.save_config()
        logger.info("Configuration reset to defaults")

# Global configuration manager instance
config_manager = ConfigManager()

def get_config() -> AppConfig:
    """Get global configuration instance"""
    return config_manager.config

def get_database_config() -> DatabaseConfig:
    """Get database configuration"""
    return config_manager.get_database_config()

def get_ui_config() -> UIConfig:
    """Get UI configuration"""
    return config_manager.get_ui_config()

def get_security_config() -> SecurityConfig:
    """Get security configuration"""
    return config_manager.get_security_config()

def get_performance_config() -> PerformanceConfig:
    """Get performance configuration"""
    return config_manager.get_performance_config()

def get_ai_config() -> AIConfig:
    """Get AI configuration"""
    return config_manager.get_ai_config()
