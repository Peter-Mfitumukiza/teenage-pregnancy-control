# Create this file as src/utils/security.py OR add this function to your existing security.py

import html
import re

def sanitize_text(text):
    """Sanitize text for safe database storage and display"""
    if not text:
        return ""
    
    # HTML escape
    text = html.escape(text)
    
    # Remove script tags and javascript
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    
    return text.strip()
