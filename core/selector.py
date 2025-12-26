"""Selector API."""
from typing import Optional
from core.element import Element
from core.parser import parse_xml
from core.utils import normalize_text


def find(xml_path: str, text: str = None, text_contains: str = None,
         resource_id: str = None, class_name: str = None,
         tappable: bool = True, nth: int = 0) -> Optional[Element]:
    """
    Find element in XML file.
    
    Args:
        xml_path: Path to XML file
        text: Exact text to match (normalized)
        text_contains: Text substring to match (normalized)
        resource_id: Resource ID to match
        class_name: Class name to match
        tappable: Filter out non-tappable elements (default: True)
        nth: Index of element to return when multiple matches (0-based, default: 0)
        
    Returns:
        Element if found, None otherwise
    """
    elements = parse_xml(xml_path)
    
    # Normalize search text
    normalized_text = normalize_text(text) if text is not None else None
    normalized_contains = normalize_text(text_contains) if text_contains is not None else None
    
    matched_elements = []
    
    for element in elements:
        # Filter tappable
        if tappable and not element.is_tappable():
            continue
        
        # Match resource_id
        if resource_id is not None and element.resource_id != resource_id:
            continue
        
        # Match class_name
        if class_name is not None and element.class_name != class_name:
            continue
        
        # Match text (exact or contains)
        display_text = element.get_display_text()
        normalized_display = normalize_text(display_text)
        
        if normalized_text is not None:
            if normalized_display != normalized_text:
                continue
        
        if normalized_contains is not None:
            if normalized_contains not in normalized_display:
                continue
        
        matched_elements.append(element)
    
    # Return nth element (0-based)
    if nth < len(matched_elements):
        return matched_elements[nth]
    
    return None

