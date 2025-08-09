"""
Telecom KPI Dashboard Version Information

This module provides version information for the entire application.
Used by app.py, health_check.py, and other modules that need version data.
"""

__version__ = "2.2.0"
__version_info__ = (2, 2, 0)

# Application metadata
APP_NAME = "Telecom KPI Dashboard"
APP_DESCRIPTION = "Production-ready KPI dashboard for telecom operators"
APP_VERSION = __version__

# Version components for programmatic access
MAJOR_VERSION = 2
MINOR_VERSION = 2
PATCH_VERSION = 0

def get_version_string() -> str:
    """Get formatted version string for display"""
    return f"{APP_NAME} v{__version__}"

def get_version_dict() -> dict:
    """Get version information as dictionary"""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "app_name": APP_NAME,
        "description": APP_DESCRIPTION
    }
