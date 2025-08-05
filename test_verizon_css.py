#!/usr/bin/env python3
"""
Test script to check Verizon theme CSS
"""

import streamlit as st
from theme_manager import switch_theme, get_current_theme_css

# Switch to Verizon theme
switch_theme('verizon')

# Get the CSS
css = get_current_theme_css()

print("Current theme CSS length:", len(css))
print("First 500 characters:")
print(css[:500])

# Test if CSS contains expected Verizon variables
if '--vz-red: #cd040b' in css:
    print("✅ Verizon red color found in CSS")
else:
    print("❌ Verizon red color NOT found in CSS")

if '--vz-black: #0a0a0a' in css:
    print("✅ Verizon black color found in CSS")
else:
    print("❌ Verizon black color NOT found in CSS")

if '.verizon-topbar' in css:
    print("✅ Verizon topbar class found in CSS")
else:
    print("❌ Verizon topbar class NOT found in CSS") 