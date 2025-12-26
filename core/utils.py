"""Utility functions."""
import re
from typing import Optional, Dict


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison.
    
    Args:
        text: Raw text string
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Strip whitespace
    normalized = text.strip()
    
    # Replace newlines and tabs with space
    normalized = normalized.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    
    # Collapse multiple spaces to single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    return normalized


def parse_bounds(bounds: str) -> Optional[Dict[str, int]]:
    """
    Parse bounds string to coordinates.
    
    Args:
        bounds: Bounds string like "[x1,y1][x2,y2]"
        
    Returns:
        Dict with x1, y1, x2, y2 or None if invalid
    """
    if not bounds:
        return None
    
    try:
        # Format: [x1,y1][x2,y2]
        # Remove all brackets and split by comma
        bounds_str = bounds.replace("[", "").replace("]", "")
        # Split by comma - should give 4 parts: x1, y1, x2, y2
        parts = bounds_str.split(",")
        if len(parts) == 4:
            x1 = int(parts[0])
            y1 = int(parts[1])
            x2 = int(parts[2])
            y2 = int(parts[3])
            
            return {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            }
        # Try regex approach for format [x1,y1][x2,y2]
        import re
        match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
        if match:
            return {
                "x1": int(match.group(1)),
                "y1": int(match.group(2)),
                "x2": int(match.group(3)),
                "y2": int(match.group(4))
            }
    except (ValueError, IndexError, AttributeError):
        pass
    
    return None

