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
        
        # Remove scripts
        for script in soup.find_all('script'):
            script.decompose()
            
        # Remove styles
        for style in soup.find_all('style'):
            style.decompose()
            
        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
            
        # Remove doctype
        for doctype in soup.find_all(string=lambda text: isinstance(text, Doctype)):
            doctype.extract()
            
        # Remove meta tags
        for meta in soup.find_all('meta'):
            meta.decompose()
            
        # Remove link tags
        # for link in soup.find_all('link'):
        #     link.decompose()
            
        # Try to find relevant content around the button_text
        # if button_text:
        #     # Find all elements containing the button text
        #     button_elements = []
            
            # # Try to find exact button elements first
            # for button in soup.find_all('button'):
            #     if button.text and button_text.lower() in button.text.lower():
            #         button_elements.append(button)
            
            # # If no buttons found, try other elements like anchors or divs
            # if not button_elements:
            #     for elem in soup.find_all(['a', 'div', 'span', 'input']):
            #         if elem.text and button_text.lower() in elem.text.lower():
            #             button_elements.append(elem)
            
            # # If button elements found, extract relevant content
            # if button_elements:
            #     # Keep track of found context
            #     context_elements = set()
                
            #     for button in button_elements:
            #         # Add the button itself
            #         context_elements.add(button)
                    
            #         # Add parent elements (up to 3 levels)
            #         parent = button.parent
            #         level = 0
            #         while parent and level < 3:
            #             context_elements.add(parent)
            #             parent = parent.parent
            #             level += 1
                    
            #         # For each parent, keep their direct children
            #         for parent_elem in list(context_elements):
            #             if hasattr(parent_elem, 'children'):
            #                 for child in parent_elem.children:
            #                     if child.name:  # Skip NavigableString
            #                         context_elements.add(child)
                
            #     # Create a new soup with just the relevant elements
            #     new_soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
            #     container = new_soup.body
                
            #     # Sort elements by their location in the original document
            #     sorted_elements = sorted(context_elements, key=lambda x: str(x).count('<'))
                
            #     # Add elements to the new soup
            #     for elem in sorted_elements:
            #         if hasattr(elem, 'name') and elem.name:
            #             # Avoid duplicating body or html
            #             if elem.name not in ['html', 'body']:
            #                 container.append(elem)
                
            #     # Only use the new soup if it contains the button text
            #     if button_text.lower() in new_soup.text.lower():
            #         soup = new_soup
        
        # Convert back to string
        cleaned_html = str(soup)
        
        if ultra_compact:
            # Ultra compact mode - create a single line with minimal whitespace
            # 1. Remove all newlines
            cleaned_html = cleaned_html.replace('\n', '')
            
            # 2. Remove whitespace between tags
            cleaned_html = re.sub(r'>\s+<', '><', cleaned_html)
            
            # 3. Compress multiple spaces to single space inside tags
            cleaned_html = re.sub(r' {2,}', ' ', cleaned_html)
            
            # 4. Remove spaces around tag attributes
            cleaned_html = re.sub(r'\s*=\s*', '=', cleaned_html)
            
        else:
            # Standard whitespace cleaning
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
        
        # Calculate reduction
        reduction_percent = ((original_size - new_size) / original_size) * 100
        
        return cleaned_html, original_size, new_size
    except Exception as e:
        print(f"Error cleaning HTML: {str(e)}")
        return full_html, len(full_html), len(full_html)
