"""Element abstraction."""
from typing import Optional, Tuple
from core import device
from core.utils import parse_bounds


class Element:
    """UI element representation."""
    
    def __init__(self, text: str = "", resource_id: str = "", 
                 class_name: str = "", bounds: str = "", content_desc: str = "",
                 clickable: bool = False):
        """
        Initialize element.
        
        Args:
            text: Element text
            resource_id: Resource ID
            class_name: Class name
            bounds: Bounds string like "[x1,y1][x2,y2]"
            content_desc: Content description
            clickable: Whether element is clickable
        """
        self.text = text
        self.resource_id = resource_id
        self.class_name = class_name
        self.bounds = bounds
        self.content_desc = content_desc
        self.clickable = clickable
    
    def center(self) -> Tuple[int, int]:
        """
        Get center coordinates.
        
        Returns:
            Tuple of (x, y)
            
        Raises:
            ValueError: If bounds cannot be parsed
        """
        bounds_dict = parse_bounds(self.bounds)
        if bounds_dict is None:
            raise ValueError(f"Cannot parse bounds: {self.bounds}")
        
        x = (bounds_dict['x1'] + bounds_dict['x2']) // 2
        y = (bounds_dict['y1'] + bounds_dict['y2']) // 2
        return x, y
    
    def click(self) -> None:
        """Click element at center."""
        from commons.logger import log_click
        x, y = self.center()
        display_text = self.get_display_text()[:30] if self.get_display_text() else "(no text)"
        log_click(f"Clicking element at ({x}, {y}) - text: '{display_text}'")
        device.tap(x, y)
        log_click("Click executed")
    
    def exists(self) -> bool:
        """
        Check if element exists (has valid bounds).
        
        Returns:
            True if element has valid bounds
        """
        return parse_bounds(self.bounds) is not None
    
    def is_tappable(self) -> bool:
        """
        Check if element is tappable.
        
        Returns:
            True if element has valid bounds and area > 0
        """
        bounds_dict = parse_bounds(self.bounds)
        if bounds_dict is None:
            return False
        
        width = bounds_dict['x2'] - bounds_dict['x1']
        height = bounds_dict['y2'] - bounds_dict['y1']
        
        # Element is tappable if it has valid bounds with area > 0
        # We can tap on any element with valid bounds, even if not explicitly clickable
        return width > 0 and height > 0
    
    def get_display_text(self) -> str:
        """
        Get display text with fallback to content-desc.
        
        Returns:
            Text or content-desc if text is empty
        """
        if self.text:
            return self.text
        return self.content_desc

