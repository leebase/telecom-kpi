"""
🎨 Theme Switcher Component
Allows users to switch between different visual themes
"""

import streamlit as st
from theme_manager import get_available_themes, switch_theme, get_current_theme

def create_theme_switcher():
    """
    Creates a theme switcher component
    """
    st.sidebar.markdown("### 🎨 Theme")
    
    available_themes = get_available_themes()
    current_theme = get_current_theme()
    
    selected_theme = st.sidebar.selectbox(
        "Choose Theme",
        available_themes,
        index=available_themes.index(current_theme) if current_theme in available_themes else 0,
        help="Select a visual theme for the dashboard"
    )
    
    if selected_theme != current_theme:
        if switch_theme(selected_theme):
            st.sidebar.success(f"Switched to {selected_theme} theme")
            st.rerun()
        else:
            st.sidebar.error("Failed to switch theme")
    
    # Show current theme info
    st.sidebar.markdown(f"**Current:** {current_theme.title()}")
    
    return selected_theme

def create_theme_info():
    """
    Creates theme information display
    """
    st.sidebar.markdown("### ℹ️ Theme Info")
    
    available_themes = get_available_themes()
    current_theme = get_current_theme()
    
    st.sidebar.markdown(f"**Available Themes:** {len(available_themes)}")
    
    for theme in available_themes:
        if theme == current_theme:
            st.sidebar.markdown(f"✅ **{theme.title()}** (current)")
        else:
            st.sidebar.markdown(f"• {theme.title()}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("💡 **Tip:** Themes can be customized by editing the theme files.")

# Example usage:
# import streamlit as st
# from theme_switcher import create_theme_switcher
# 
# # In your main app
# create_theme_switcher() 