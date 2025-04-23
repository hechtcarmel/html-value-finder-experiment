from typing import List, Dict, Any, Optional, Tuple
from bs4 import BeautifulSoup, Comment, Doctype
import re

def clean_html(full_html: str, button_text: str, ultra_compact: bool = False) -> Tuple[str, int, int]:
    """
    Clean HTML to reduce tokens by removing unnecessary elements and focusing on
    button-relevant content.
    
    Args:
        full_html: Complete HTML content
        button_text: Text of the clicked button
        ultra_compact: If True, produces single-line minified HTML with no formatting
        
    Returns:
        Tuple of (cleaned_html, original_size, new_size)
    """
    try:
        # Track sizes for reporting
        original_size = len(full_html)
        
        # Parse HTML
        soup = BeautifulSoup(full_html, 'html.parser')
        
        # First pass of aggressive removal (elements typically not relevant for price extraction)
        for element in soup.find_all(['script', 'style', 'meta', 'svg', 'link', 'iframe', 'noscript', 'video', 'audio']):
            element.decompose()
        
        # Remove all comments and doctypes
        for comment in soup.find_all(string=lambda text: isinstance(text, (Comment, Doctype))):
            comment.extract()
                
        # Remove all class and id attributes which are usually for styling
        for tag in soup.find_all(True):
            if tag.has_attr('class'):
                del tag['class']
            if tag.has_attr('id'):
                del tag['id']
            
            # Remove data attributes and event handlers
            attrs_to_remove = [attr for attr in tag.attrs if attr.startswith('data-') or attr.startswith('on')]
            for attr in attrs_to_remove:
                del tag[attr]
        
        # Remove empty elements that don't contribute to the structure
        for tag in soup.find_all():
            if not tag.contents and tag.name not in ['img', 'br', 'hr', 'input']:
                tag.decompose()
        
        cleaned_html = str(soup)
        
        if ultra_compact:
            # Ultra compact mode - more aggressive than before
            # 1. Remove all newlines
            cleaned_html = cleaned_html.replace('\n', '')
            
            # 2. Remove whitespace between tags
            cleaned_html = re.sub(r'>\s+<', '><', cleaned_html)
            
            # 3. Compress multiple spaces to single space inside tags
            cleaned_html = re.sub(r' {2,}', ' ', cleaned_html)
            
            # 4. Remove spaces around tag attributes
            cleaned_html = re.sub(r'\s*=\s*', '=', cleaned_html)
            
            # 5. Remove unnecessary quotes around attribute values when safe
            cleaned_html = re.sub(r'="([a-zA-Z0-9_-]+)"', r'=\1', cleaned_html)
            
            # 6. Remove empty attributes
            cleaned_html = re.sub(r'\s+[a-zA-Z-]+=("")', '', cleaned_html)
        else:
            # Standard cleaning
            # 1. Replace multiple newlines with a single newline
            cleaned_html = re.sub(r'\n\s*\n', '\n', cleaned_html)
            
            # 2. Remove leading/trailing whitespace from each line
            cleaned_html = '\n'.join(line.strip() for line in cleaned_html.split('\n'))
            
            # 3. Remove empty lines
            cleaned_html = '\n'.join(line for line in cleaned_html.split('\n') if line.strip())
            
            # 4. Compress multiple spaces to single space
            cleaned_html = re.sub(r' {2,}', ' ', cleaned_html)
            
            # 5. Remove whitespace between tags
            cleaned_html = re.sub(r'>\s+<', '><', cleaned_html)
        
        new_size = len(cleaned_html)
        
        return cleaned_html, original_size, new_size
    except Exception as e:
        print(f"Error cleaning HTML: {str(e)}")
        return full_html, len(full_html), len(full_html)