"""
🎨 Cognizant Theme Module
Modular styling system for Telecom KPI Dashboard
Based on the UX design specification
"""

def get_cognizant_css():
    """
    Returns the Cognizant-inspired CSS styling from external file
    """
    import os
    
    css_file_path = os.path.join("styles", "cognizant", "cognizant.css")
    
    try:
        with open(css_file_path, 'r') as f:
            css_content = f.read()
        return f"<style>{css_content}</style>"
    except FileNotFoundError:
        # Fallback to inline CSS if file not found
        return """
        <style>
        /* Fallback Cognizant Theme */
        .stApp {
            background: linear-gradient(180deg, #061023 0%, #0b152a 60%, #0d1730 100%);
            color: #e6effa;
        }
        </style>
        """

def create_cognizant_header():
    """
    Creates the Cognizant-style header with logo
    """
    import os
    
    logo_path = os.path.join("styles", "cognizant", "logojpg.jpg")
    
    # Check if logo exists, otherwise use fallback
    if os.path.exists(logo_path):
        logo_html = f'<img src="data:image/jpeg;base64,{get_base64_image(logo_path)}" alt="Cognizant Logo" />'
    else:
        logo_html = '<div class="cognizant-brand-logo" aria-hidden="true"></div>'
    
    return f"""
    <div class="cognizant-topbar">
        <div class="cognizant-topbar-inner">
            <div class="cognizant-brand" aria-label="Cognizant Telecom Dashboard">
                <div class="cognizant-brand-logo">
                    {logo_html}
                </div>
                <div>
                    <div class="cognizant-brand-name">Cognizant</div>
                    <div class="cognizant-brand-sub">Telecom KPI Dashboard</div>
                </div>
            </div>
            <nav class="cognizant-topbar-actions" aria-label="Global actions">
                <button class="btn" type="button">Export</button>
                <button class="btn" type="button">Share</button>
                <button class="btn primary" type="button">Create Alert</button>
            </nav>
        </div>
    </div>
    """

def get_base64_image(image_path):
    """
    Converts an image file to base64 string
    """
    import base64
    
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        return ""

def create_cognizant_page_header(title, description):
    """
    Creates the Cognizant-style page header
    """
    return f"""
    <div class="cognizant-page-header">
        <div class="cognizant-title-block">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
    </div>
    """

def create_cognizant_kpi_tile(label, value, delta, delta_type="up", footer_left="", footer_right=""):
    """
    Creates a Cognizant-style KPI tile
    """
    arrow_class = f"cognizant-kpi-delta {delta_type}"
    return f"""
    <div class="cognizant-kpi-tile">
        <div class="cognizant-kpi-head">
            <div class="cognizant-kpi-label">{label}</div>
            <div class="cognizant-kpi-updated">Updated: {get_current_timestamp()}</div>
        </div>
        <div class="cognizant-kpi-value">{value}</div>
        <div class="{arrow_class}">
            <span class="arrow" aria-hidden="true"></span>
            <span>{delta}</span>
        </div>
        <div class="cognizant-sparkline" aria-hidden="true">
            <div class="line" style="top: 38%"></div>
        </div>
        <div class="cognizant-kpi-footer">
            <span>{footer_left}</span>
            <span>{footer_right}</span>
        </div>
    </div>
    """

def create_cognizant_section_card(title, subtitle, content):
    """
    Creates a Cognizant-style section card
    """
    return f"""
    <div class="cognizant-section-card">
        <div class="cognizant-section-header">
            <h2 class="cognizant-section-title">{title}</h2>
            <div class="cognizant-section-sub">{subtitle}</div>
        </div>
        {content}
    </div>
    """

def get_current_timestamp():
    """
    Returns current timestamp in the format used by the design
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M")

# Theme configuration
THEME_CONFIG = {
    "name": "Cognizant",
    "version": "1.0.0",
    "description": "Cognizant-inspired dark theme with deep blues and cyan accents",
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
} 