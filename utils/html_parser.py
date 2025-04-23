from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

def extract_relevant_html(
    full_html: str, 
    click_path: List[str], 
    context_size: int = 5
) -> str:
    """
    Extract relevant portion of HTML around the clicked element.
    
    Args:
        full_html: Complete HTML content
        click_path: CSS selectors path to the clicked element
        context_size: Number of siblings to include for context
        
    Returns:
        Extracted HTML with relevant context
    """
    try:
        soup = BeautifulSoup(full_html, 'html.parser')
        
        # Find the clicked element
        element = soup
        for selector in click_path:
            if selector.startswith("#"):
                element = element.find(id=selector[1:])
            elif selector.startswith("."):
                element = element.find(class_=selector[1:])
            elif "." in selector:
                tag, class_name = selector.split(".", 1)
                element = element.find(tag, class_=class_name)
            elif "#" in selector:
                tag, id_name = selector.split("#", 1)
                element = element.find(tag, id=id_name)
            else:
                element = element.find(selector)
                
            if not element:
                return ""
        
        # Get parent container
        parent = element.parent
        
        # Extract relevant siblings for context
        siblings = []
        for i, sibling in enumerate(parent.children):
            if i < context_size * 2 + 1:
                siblings.append(str(sibling))
        
        # If we can go up another level for more context, do so
        if parent.parent:
            return str(parent.parent)
        
        return "".join(siblings)
    except Exception as e:
        print(f"Error parsing HTML: {str(e)}")
        return full_html[:1000]  # Return truncated HTML on error 