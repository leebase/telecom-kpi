"""
Centralized Logging Configuration

This module provides a unified logging configuration system for the Telecom Dashboard
with different log levels, formatters, and handlers for different components.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Dict, Optional, Union
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Custom formatter with color coding for different log levels"""
    
    # Color codes for different log levels
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']
        
        # Format the timestamp
        record.asctime = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Color the level name
        original_levelname = record.levelname
        record.levelname = f"{log_color}{record.levelname:8}{reset_color}"
        
        # Format the message
        formatted = super().format(record)
        
        # Restore original levelname for other handlers
        record.levelname = original_levelname
        
        return formatted

class LoggingConfig:
    """Centralized logging configuration manager"""
    
    def __init__(self, 
                 log_dir: str = "logs",
                 console_level: str = "INFO",
                 file_level: str = "DEBUG",
                 enable_colors: bool = True):
        """
        Initialize logging configuration
        
        Args:
            log_dir: Directory for log files
            console_level: Log level for console output
            file_level: Log level for file output
            enable_colors: Whether to use colored console output
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.console_level = getattr(logging, console_level.upper())
        self.file_level = getattr(logging, file_level.upper())
        self.enable_colors = enable_colors
        self._configured_loggers = set()
        
        # Configure root logger
        self._setup_root_logger()
    
    def _setup_root_logger(self):
        """Setup the root logger with basic configuration"""
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.console_level)
        
        if self.enable_colors and sys.stdout.isatty():
            console_formatter = ColoredFormatter(
                '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
            )
        else:
            console_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
            )
        
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
        # File handler for general logs
        self._add_file_handler(root_logger, "application.log")
    
    def _add_file_handler(self, logger: logging.Logger, filename: str):
        """Add a rotating file handler to a logger"""
        log_file = self.log_dir / filename
        
        # Use RotatingFileHandler for automatic log rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(self.file_level)
        
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    def get_logger(self, name: str, 
                   level: Optional[Union[str, int]] = None,
                   log_file: Optional[str] = None) -> logging.Logger:
        """
        Get a configured logger for a specific component
        
        Args:
            name: Logger name (usually module name)
            level: Optional specific log level for this logger
            log_file: Optional specific log file for this logger
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        
        # Avoid reconfiguring already configured loggers
        if name in self._configured_loggers:
            return logger
        
        if level is not None:
            if isinstance(level, str):
                level = getattr(logging, level.upper())
            logger.setLevel(level)
        
        # Add specific file handler if requested
        if log_file:
            self._add_file_handler(logger, log_file)
            # Prevent propagation to avoid duplicate logs
            logger.propagate = False
            
            # Add console handler for this specific logger
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.console_level)
            
            if self.enable_colors and sys.stdout.isatty():
                console_formatter = ColoredFormatter(
                    '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
                )
            else:
                console_formatter = logging.Formatter(
                    '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
                )
            
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        self._configured_loggers.add(name)
        return logger
    
    def configure_component_loggers(self):
        """Configure specific loggers for different application components"""
        
        # Database operations logger
        db_logger = self.get_logger('database', level='DEBUG', log_file='database.log')
        
        # Security logger (already exists but ensure it's properly configured)
        security_logger = self.get_logger('security', level='INFO', log_file='security.log')
        
        # AI/LLM logger
        ai_logger = self.get_logger('ai_insights', level='INFO', log_file='ai_insights.log')
        
        # Performance logger
        perf_logger = self.get_logger('performance', level='INFO', log_file='performance.log')
        
        # UI logger
        ui_logger = self.get_logger('ui', level='WARNING', log_file='ui.log')
        
        return {
            'database': db_logger,
            'security': security_logger,
            'ai_insights': ai_logger,
            'performance': perf_logger,
            'ui': ui_logger
        }

# Global logging configuration
_logging_config = None

def setup_logging(log_dir: str = "logs",
                  console_level: str = "INFO",
                  file_level: str = "DEBUG",
                  enable_colors: bool = True) -> LoggingConfig:
    """
    Setup global logging configuration
    
    Args:
        log_dir: Directory for log files
        console_level: Log level for console output
        file_level: Log level for file output
        enable_colors: Whether to use colored console output
        
    Returns:
        Configured LoggingConfig instance
    """
    global _logging_config
    _logging_config = LoggingConfig(
        log_dir=log_dir,
        console_level=console_level,
        file_level=file_level,
        enable_colors=enable_colors
    )
    return _logging_config

def get_logger(name: str, 
               level: Optional[Union[str, int]] = None,
               log_file: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance using global configuration
    
    Args:
        name: Logger name
        level: Optional log level
        log_file: Optional log file
        
    Returns:
        Configured logger instance
    """
    global _logging_config
    if _logging_config is None:
        _logging_config = setup_logging()
    
    return _logging_config.get_logger(name, level, log_file)

def configure_app_logging():
    """Configure logging for the entire application"""
    global _logging_config
    if _logging_config is None:
        _logging_config = setup_logging()
    
    # Configure component loggers
    loggers = _logging_config.configure_component_loggers()
    
    # Log startup message
    app_logger = get_logger('application')
    app_logger.info("Telecom Dashboard logging system initialized")
    app_logger.info(f"Log directory: {_logging_config.log_dir}")
    app_logger.info(f"Console level: {logging.getLevelName(_logging_config.console_level)}")
    app_logger.info(f"File level: {logging.getLevelName(_logging_config.file_level)}")
    
    return loggers

# Convenience functions for common logging patterns
def log_performance(operation: str, duration: float, details: Optional[Dict] = None):
    """Log performance metrics"""
    perf_logger = get_logger('performance')
    message = f"{operation} completed in {duration:.3f}s"
    if details:
        message += f" | Details: {details}"
    perf_logger.info(message)

def log_database_operation(operation: str, table: Optional[str] = None, 
                          duration: Optional[float] = None):
    """Log database operations"""
    db_logger = get_logger('database')
    message = f"Database operation: {operation}"
    if table:
        message += f" | Table: {table}"
    if duration:
        message += f" | Duration: {duration:.3f}s"
    db_logger.info(message)

def log_security_event(event_type: str, details: str, level: str = "INFO"):
    """Log security events"""
    security_logger = get_logger('security')
    log_level = getattr(logging, level.upper())
    security_logger.log(log_level, f"{event_type}: {details}")

def log_ai_operation(operation: str, model: Optional[str] = None, 
                    tokens: Optional[int] = None, duration: Optional[float] = None):
    """Log AI/LLM operations"""
    ai_logger = get_logger('ai_insights')
    message = f"AI operation: {operation}"
    if model:
        message += f" | Model: {model}"
    if tokens:
        message += f" | Tokens: {tokens}"
    if duration:
        message += f" | Duration: {duration:.3f}s"
    ai_logger.info(message)
