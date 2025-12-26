"""XML parser for UI elements."""
import xml.etree.ElementTree as ET
from typing import List
from core.element import Element


def parse_xml(file_path: str) -> List[Element]:
    """
    Parse XML file and return list of elements.
    
    Args:
        file_path: Path to XML file
        
    Returns:
        List of Element objects
    """
    # Parse with explicit UTF-8 encoding handling
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
    root = tree.getroot()
    
    elements = []
    for node in root.iter():
        bounds = node.get("bounds", "")
        text = node.get("text", "")
        resource_id = node.get("resource-id", "")
        class_name = node.get("class", "")
        content_desc = node.get("content-desc", "")
        clickable_str = node.get("clickable", "false")
        clickable = clickable_str.lower() == "true"
        
        element = Element(
            text=text,
            resource_id=resource_id,
            class_name=class_name,
            bounds=bounds,
            content_desc=content_desc,
            clickable=clickable
        )
        elements.append(element)
    
    return elements

