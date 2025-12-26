"""Wait and retry mechanism."""
import time
from typing import Callable, Optional
from core import dump
from core.selector import find
from core.element import Element
from core.exceptions import TimeoutException
from config import settings


class Wait:
    """Wait for condition or element."""
    
    def __init__(self, timeout: float = None, interval: float = 1.0):
        """
        Initialize wait.
        
        Args:
            timeout: Timeout in seconds (uses config default if None)
            interval: Polling interval in seconds
        """
        self.timeout = timeout or settings.TIMEOUT
        self.interval = interval
    
    def until(self, condition_fn: Callable[[], bool]) -> bool:
        """
        Wait until condition is true.
        
        Args:
            condition_fn: Function that returns True when condition is met
            
        Returns:
            True when condition is met
            
        Raises:
            TimeoutException: If timeout is reached
        """
        start_time = time.time()
        
        while True:
            if condition_fn():
                return True
            
            if time.time() - start_time >= self.timeout:
                raise TimeoutException(f"Timeout after {self.timeout}s")
            
            time.sleep(self.interval)
    
    def until_element(self, text: str = None, text_contains: str = None,
                     resource_id: str = None, class_name: str = None,
                     tappable: bool = True, nth: int = 0) -> Element:
        """
        Wait until element is found.
        
        Args:
            text: Exact text to match
            text_contains: Text substring to match
            resource_id: Resource ID to match
            class_name: Class name to match
            tappable: Filter out non-tappable elements (default: True)
            nth: Index of element to return when multiple matches (0-based, default: 0)
            
        Returns:
            Element when found
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        start_time = time.time()
        attempt = 0
        
        # Build search description
        search_desc = []
        if text is not None:
            search_desc.append(f"text='{text}'")
        if text_contains is not None:
            search_desc.append(f"text_contains='{text_contains}'")
        if resource_id is not None:
            search_desc.append(f"resource_id='{resource_id}'")
        if class_name is not None:
            search_desc.append(f"class_name='{class_name}'")
        if nth > 0:
            search_desc.append(f"nth={nth}")
        search_str = ", ".join(search_desc) if search_desc else "any element"
        
        print(f"[WAIT] Looking for element: {search_str} (timeout={self.timeout}s)")
        
        while True:
            attempt += 1
            elapsed = time.time() - start_time
            print(f"[WAIT] Attempt {attempt} (elapsed: {elapsed:.1f}s)...")
            
            xml_path, _ = dump.dump_ui("wait")
            
            # Validate XML file exists and has content
            import os
            if not os.path.exists(xml_path) or os.path.getsize(xml_path) == 0:
                print(f"[WAIT] XML dump failed or empty")
                if time.time() - start_time >= self.timeout:
                    raise TimeoutException(
                        f"XML dump failed or empty after {self.timeout}s "
                        f"(xml_path={xml_path})"
                    )
                time.sleep(self.interval)
                continue
            
            element = find(xml_path, text=text, text_contains=text_contains,
                          resource_id=resource_id, class_name=class_name,
                          tappable=tappable, nth=nth)
            
            if element is not None:
                display_text = element.get_display_text()[:30] if element.get_display_text() else "(no text)"
                print(f"[WAIT] ✓ Element found after {elapsed:.1f}s: '{display_text}'")
                return element
            
            print(f"[WAIT] ✗ Element not found, retrying in {self.interval}s...")
            
            if time.time() - start_time >= self.timeout:
                # Get available texts for debugging
                from core.parser import parse_xml
                from core.utils import normalize_text
                try:
                    elements = parse_xml(xml_path)
                    available_texts = set()
                    all_elements_count = len(elements)
                    tappable_count = 0
                    
                    for el in elements:
                        if el.is_tappable():
                            tappable_count += 1
                        if not tappable or el.is_tappable():
                            display_text = el.get_display_text()
                            if display_text:
                                normalized = normalize_text(display_text)
                                if normalized:
                                    available_texts.add(normalized)
                    
                    available_list = sorted(list(available_texts))[:20]  # Limit to 20
                    available_str = ", ".join(available_list) if available_list else "(none)"
                    
                    raise TimeoutException(
                        f"Element not found within {self.timeout}s "
                        f"(text={text}, text_contains={text_contains}, "
                        f"resource_id={resource_id}, class_name={class_name}, nth={nth})\n"
                        f"Total elements: {all_elements_count}, "
                        f"Tappable: {tappable_count}\n"
                        f"Available texts: {available_str}"
                    )
                except Exception as e:
                    raise TimeoutException(
                        f"Element not found within {self.timeout}s "
                        f"(text={text}, text_contains={text_contains}, "
                        f"resource_id={resource_id}, class_name={class_name}, nth={nth})\n"
                        f"Error parsing XML: {e}"
                    )
            
            time.sleep(self.interval)

