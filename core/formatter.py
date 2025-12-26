"""XML formatter."""
import xml.dom.minidom


def format_xml(file_path: str) -> str:
    """
    Format XML file for readability.
    
    Args:
        file_path: Path to XML file
        
    Returns:
        Formatted XML string
    """
    dom = xml.dom.minidom.parse(file_path)
    return dom.toprettyxml(indent="  ")

