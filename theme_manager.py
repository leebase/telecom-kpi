"""
🎨 Theme Manager
Modular theme system for Telecom KPI Dashboard
Allows easy switching between different visual themes
"""

from cognizant_theme import get_cognizant_css, create_cognizant_header, create_cognizant_page_header
from verizon_theme import get_verizon_css, create_verizon_header, get_verizon_page_header

class ThemeManager:
    """
    Manages different visual themes for the dashboard
    """
    
    def __init__(self):
        self.themes = {
            "cognizant": {
                "name": "Cognizant",
                "description": "Cognizant-inspired dark theme with deep blues and cyan accents",
                "css_function": get_cognizant_css,
                "header_function": create_cognizant_header,
                "page_header_function": create_cognizant_page_header,
                "colors": {
                    "primary": "#00bcd4",
                    "secondary": "#00a3d9",
                    "success": "#3ad29f",
                    "danger": "#ff6b6b",
                    "warning": "#ffc857",
                    "background": "#0a1222",
                    "surface": "#13223d",
                    "text": "#e6effa",
                    "text_muted": "#a7b3c7"
                }
            },
            "verizon": {
                "name": "Verizon",
                "description": "Verizon pitch theme with bold blacks and red accents",
                "css_function": get_verizon_css,
                "header_function": create_verizon_header,
                "page_header_function": get_verizon_page_header,
                "colors": {
                    "primary": "#cd040b",
                    "secondary": "#ff4b51",
                    "success": "#2ecc71",
                    "danger": "#cd040b",
                    "warning": "#f5a623",
                    "background": "#0a0a0a",
                    "surface": "#1b1d21",
                    "text": "#f5f7fa",
                    "text_muted": "#b7c0cc"
                }
            }
            # Future themes can be added here:
            # "light": { ... },
            # "corporate": { ... },
            # "modern": { ... }
        }
        self.current_theme = "cognizant"
    
    def get_available_themes(self):
        """
        Returns list of available theme names
        """
        return list(self.themes.keys())
    
    def get_current_theme(self):
        """
        Returns the current theme name
        """
        return self.current_theme
    
    def set_theme(self, theme_name):
        """
        Sets the current theme
        """
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def get_css(self):
        """
        Returns CSS for the current theme
        """
        theme = self.themes[self.current_theme]
        return theme["css_function"]()
    
    def get_header(self):
        """
        Returns header HTML for the current theme
        """
        theme = self.themes[self.current_theme]
        return theme["header_function"]()
    
    def get_page_header(self, title, description):
        """
        Returns page header HTML for the current theme
        """
        theme = self.themes[self.current_theme]
        return theme["page_header_function"](title, description)
    
    def get_theme_info(self, theme_name=None):
        """
        Returns information about a theme
        """
        if theme_name is None:
            theme_name = self.current_theme
        
        if theme_name in self.themes:
            theme = self.themes[theme_name]
            return {
                "name": theme["name"],
                "description": theme["description"],
                "colors": theme["colors"]
            }
        return None
    
    def add_theme(self, theme_name, theme_config):
        """
        Adds a new theme to the manager
        """
        self.themes[theme_name] = theme_config
    
    def remove_theme(self, theme_name):
        """
        Removes a theme from the manager
        """
        if theme_name in self.themes and theme_name != "cognizant":
            del self.themes[theme_name]
            return True
        return False

# Global theme manager instance
theme_manager = ThemeManager()

def get_current_theme_css():
    """
    Returns CSS for the current theme
    """
    return theme_manager.get_css()

def get_current_theme_header():
    """
    Returns header HTML for the current theme
    """
    return theme_manager.get_header()

def get_current_theme_page_header(title, description):
    """
    Returns page header HTML for the current theme
    """
    return theme_manager.get_page_header(title, description)

def switch_theme(theme_name):
    """
    Switches to a different theme
    """
    return theme_manager.set_theme(theme_name)

def get_current_theme():
    """
    Returns the current theme name
    """
    return theme_manager.get_current_theme()

def get_available_themes():
    """
    Returns list of available themes
    """
    return theme_manager.get_available_themes()

# Example usage:
# import streamlit as st
# from theme_manager import get_current_theme_css, get_current_theme_header
# 
# st.markdown(get_current_theme_css(), unsafe_allow_html=True)
# st.markdown(get_current_theme_header(), unsafe_allow_html=True) 