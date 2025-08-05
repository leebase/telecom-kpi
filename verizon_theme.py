"""
Verizon Theme Module for Telecom KPI Dashboard
Provides Verizon-branded styling and components
"""

import base64
import os

def get_base64_image(image_path):
    """Convert an image file to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

def get_verizon_css():
    """Get Verizon theme CSS"""
    css_file_path = "styles/verizon/verizon.css"
    
    try:
        with open(css_file_path, 'r') as f:
            css_content = f.read()
        return f"<style>{css_content}</style>"
    except FileNotFoundError:
        # Fallback to inline CSS if file not found
        return """
        <style>
        /* Verizon Theme Fallback */
        :root {
            --vz-black: #0a0a0a;
            --vz-ink: #f5f7fa;
            --vz-muted: #b7c0cc;
            --vz-card: #1b1d21;
            --vz-red: #cd040b;
            --vz-green: #2ecc71;
        }
        
        .stApp {
            background: linear-gradient(180deg, #0a0a0a 0%, #0e0e10 55%, #101114 100%);
            color: var(--vz-ink);
        }
        </style>
        """

def create_verizon_header():
    """Create Verizon header with logo"""
    logo_path = "styles/verizon/logojpg.jpg"
    logo_base64 = get_base64_image(logo_path)
    
    if logo_base64:
        logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Verizon Logo" style="width: 28px; height: 28px; object-fit: contain; border-radius: 4px;">'
    else:
        # Fallback to CSS gradient logo
        logo_html = '<div class="verizon-brand-logo" aria-hidden="true"></div>'
    
    return f"""
    <div class="verizon-topbar">
        <div class="verizon-topbar-inner">
            <div class="verizon-brand" aria-label="Verizon Telecom Dashboard">
                {logo_html}
                <div>
                    <div class="verizon-brand-name">Verizon</div>
                    <div class="verizon-brand-sub">Telecom KPI Dashboard</div>
                </div>
            </div>
            <nav class="verizon-topbar-actions" aria-label="Global actions">
                <button class="btn" type="button">Export</button>
                <button class="btn" type="button">Share</button>
                <button class="btn primary" type="button">Create Alert</button>
            </nav>
        </div>
    </div>
    """

def get_verizon_page_header(title, description):
    """Create Verizon page header"""
    return f"""
    <section class="verizon-page-header" aria-labelledby="page-title">
        <div class="verizon-title-block">
            <h1 id="page-title">{title}</h1>
            <p>{description}</p>
        </div>
        <div class="verizon-filters">
            <div class="verizon-control">
                <label for="period">Select Time Period</label>
                <select class="select" id="period" name="period">
                    <option>Last 7 Days</option>
                    <option selected>Last 12 Months</option>
                    <option>Year to Date</option>
                    <option>Previous Quarter</option>
                    <option>Custom Range</option>
                </select>
            </div>
            <div class="verizon-control">
                <label for="region">Region</label>
                <select class="select" id="region" name="region">
                    <option selected>All Regions</option>
                    <option>North</option>
                    <option>South</option>
                    <option>East</option>
                    <option>West</option>
                </select>
            </div>
        </div>
    </section>
    """ 