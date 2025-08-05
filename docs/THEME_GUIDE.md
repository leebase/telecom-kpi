# 🎨 Theme Guide - Telecom KPI Dashboard

## Overview

The Telecom KPI Dashboard uses a modular theme system that allows easy customization of the visual appearance. The current implementation includes the **Cognizant** theme, and new themes can be easily added.

## 🏗️ Architecture

### Theme System Components

1. **`cognizant_theme.py`** - Individual theme implementation
2. **`theme_manager.py`** - Central theme management system
3. **`theme_switcher.py`** - UI component for theme switching
4. **`app.py`** - Main application using theme system

### Theme Structure

Each theme must provide these functions:
- `get_css()` - Returns CSS styling
- `create_header()` - Returns header HTML
- `create_page_header(title, description)` - Returns page header HTML

## 🎯 Current Theme: Cognizant

### Design Philosophy
- **Dark theme** with deep blues and cyan accents
- **Professional appearance** suitable for enterprise use
- **High contrast** for accessibility
- **Responsive design** for all screen sizes

### Color Palette
```css
--bg: #0a1222;           /* Background */
--bg-card: #13223d;      /* Card background */
--ink: #e6effa;          /* Primary text */
--muted: #a7b3c7;       /* Secondary text */
--accent: #00bcd4;      /* Primary accent */
--accent-2: #00a3d9;    /* Secondary accent */
--success: #3ad29f;      /* Success indicators */
--danger: #ff6b6b;       /* Error indicators */
--warning: #ffc857;      /* Warning indicators */
```

## ➕ Adding New Themes

### Step 1: Create Theme File

Create a new file `your_theme.py`:

```python
"""
🎨 Your Theme Name
Description of your theme
"""

def get_your_theme_css():
    """
    Returns the CSS styling for your theme
    """
    return """
    <style>
    /* Your theme CSS here */
    :root {
        --bg: #your-background-color;
        --ink: #your-text-color;
        /* ... other variables */
    }
    
    /* Global styles */
    .stApp {
        background: your-background;
        color: var(--ink);
    }
    
    /* Component styles */
    .your-theme-kpi-tile {
        background: your-card-background;
        border: your-border;
        border-radius: your-radius;
    }
    
    /* ... more styles */
    </style>
    """

def create_your_theme_header():
    """
    Creates the header HTML for your theme
    """
    return """
    <div class="your-theme-header">
        <div class="your-theme-brand">
            <div class="your-theme-logo"></div>
            <div class="your-theme-name">Your Brand</div>
        </div>
    </div>
    """

def create_your_theme_page_header(title, description):
    """
    Creates the page header HTML for your theme
    """
    return f"""
    <div class="your-theme-page-header">
        <h1>{title}</h1>
        <p>{description}</p>
    </div>
    """

# Theme configuration
YOUR_THEME_CONFIG = {
    "name": "Your Theme Name",
    "version": "1.0.0",
    "description": "Description of your theme",
    "colors": {
        "primary": "#your-primary-color",
        "secondary": "#your-secondary-color",
        "success": "#your-success-color",
        "danger": "#your-danger-color",
        "warning": "#your-warning-color",
        "background": "#your-background-color",
        "surface": "#your-surface-color",
        "text": "#your-text-color",
        "text_muted": "#your-muted-text-color"
    }
}
```

### Step 2: Register Theme in Theme Manager

Update `theme_manager.py` to include your theme:

```python
from your_theme import get_your_theme_css, create_your_theme_header, create_your_theme_page_header

class ThemeManager:
    def __init__(self):
        self.themes = {
            "cognizant": {
                # ... existing cognizant theme
            },
            "your_theme": {
                "name": "Your Theme Name",
                "description": "Description of your theme",
                "css_function": get_your_theme_css,
                "header_function": create_your_theme_header,
                "page_header_function": create_your_theme_page_header,
                "colors": {
                    "primary": "#your-primary-color",
                    "secondary": "#your-secondary-color",
                    # ... other colors
                }
            }
        }
```

### Step 3: Test Your Theme

1. Run the application: `streamlit run app.py`
2. Use the theme switcher in the sidebar
3. Verify all components render correctly
4. Test responsiveness on different screen sizes

## 🎨 Theme Design Guidelines

### Color Considerations
- **Accessibility**: Ensure sufficient contrast ratios (WCAG 2.1 AA)
- **Branding**: Align with your organization's brand guidelines
- **Readability**: Text should be easily readable in all conditions

### Component Styling
- **KPI Tiles**: Should have clear visual hierarchy
- **Charts**: Should be readable with your color scheme
- **Navigation**: Should be intuitive and accessible
- **Responsive**: Should work on mobile and desktop

### CSS Best Practices
- Use CSS variables for consistent theming
- Include responsive breakpoints
- Provide focus states for accessibility
- Use semantic class names

## 🔧 Customization Examples

### Light Theme Example
```python
def get_light_theme_css():
    return """
    <style>
    :root {
        --bg: #ffffff;
        --bg-card: #f8f9fa;
        --ink: #212529;
        --muted: #6c757d;
        --accent: #007bff;
        --success: #28a745;
        --danger: #dc3545;
    }
    
    .stApp {
        background: var(--bg);
        color: var(--ink);
    }
    
    .light-theme-kpi-tile {
        background: var(--bg-card);
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """
```

### Corporate Theme Example
```python
def get_corporate_theme_css():
    return """
    <style>
    :root {
        --bg: #1a1a1a;
        --bg-card: #2d2d2d;
        --ink: #ffffff;
        --muted: #b0b0b0;
        --accent: #4CAF50;
        --success: #8BC34A;
        --danger: #F44336;
    }
    
    .stApp {
        background: var(--bg);
        color: var(--ink);
    }
    
    .corporate-theme-kpi-tile {
        background: var(--bg-card);
        border: 1px solid #404040;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    </style>
    """
```

## 🚀 Deployment Considerations

### Performance
- Keep CSS files lightweight
- Use efficient selectors
- Minimize repaints and reflows

### Browser Compatibility
- Test across different browsers
- Provide fallbacks for older browsers
- Ensure mobile compatibility

### Accessibility
- Maintain WCAG 2.1 AA compliance
- Provide keyboard navigation
- Include screen reader support

## 📝 Theme Documentation

When creating a new theme, document:

1. **Design Philosophy**: What inspired this theme?
2. **Color Palette**: All colors used and their purposes
3. **Typography**: Font choices and hierarchy
4. **Components**: How each component is styled
5. **Accessibility**: How accessibility is maintained
6. **Browser Support**: Which browsers are supported

## 🔄 Theme Switching

The theme system supports:
- **Dynamic switching** without page reload
- **Persistent selection** across sessions
- **Fallback handling** for missing themes
- **Error handling** for invalid themes

## 📊 Testing Checklist

Before deploying a new theme:

- [ ] All KPI tiles render correctly
- [ ] Charts are readable and accessible
- [ ] Navigation works on all screen sizes
- [ ] Print layout is optimized
- [ ] Color contrast meets WCAG standards
- [ ] Performance is acceptable
- [ ] Cross-browser compatibility verified

## 🎯 Future Enhancements

Planned improvements to the theme system:

1. **Theme Preview**: Visual preview in theme switcher
2. **Custom Themes**: User-uploadable theme files
3. **Theme Editor**: Visual theme customization tool
4. **Theme Marketplace**: Repository of community themes
5. **Auto-detection**: Automatic theme detection based on user preferences

---

**Need Help?** Check the main README.md for additional resources and contact information. 