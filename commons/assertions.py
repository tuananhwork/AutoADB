"""Assertion functions for test validation."""
from core.waiter import Wait
from core.selector import find
from core import dump
from core.exceptions import TimeoutException
from commons.logger import log_assert


class AssertionError(Exception):
    """Raised when assertion fails."""
    pass


def assert_element_exists(text_contains: str = None, text: str = None,
                         resource_id: str = None, class_name: str = None,
                         nth: int = 0, timeout: float = 5.0, message: str = None):
    """
    Assert that element exists in current UI.
    
    Args:
        text_contains: Text substring to match
        text: Exact text to match
        resource_id: Resource ID to match
        class_name: Class name to match
        nth: Index of element (0-based)
        timeout: Timeout in seconds
        message: Custom error message
        
    Raises:
        AssertionError: If element not found
    """
    try:
        element = Wait(timeout=timeout).until_element(
            text_contains=text_contains,
            text=text,
            resource_id=resource_id,
            class_name=class_name,
            nth=nth
        )
        text_display = text_contains or text or resource_id or "element"
        log_assert(f"Element exists: {text_display}", passed=True)
        return True
    except TimeoutException:
        error_msg = message or f"Element not found: text_contains={text_contains}, text={text}, resource_id={resource_id}"
        log_assert(f"FAILED: {error_msg}", passed=False)
        raise AssertionError(error_msg)


def assert_element_not_exists(text_contains: str = None, text: str = None,
                             resource_id: str = None, class_name: str = None,
                             timeout: float = 3.0, message: str = None):
    """
    Assert that element does NOT exist in current UI.
    
    Args:
        text_contains: Text substring to match
        text: Exact text to match
        resource_id: Resource ID to match
        class_name: Class name to match
        timeout: Timeout in seconds (element should not appear within this time)
        message: Custom error message
        
    Raises:
        AssertionError: If element is found
    """
    xml_path, _ = dump.dump_ui("assert")
    element = find(xml_path, text_contains=text_contains, text=text,
                  resource_id=resource_id, class_name=class_name, tappable=False)
    
    if element is not None:
        error_msg = message or f"Element should not exist but found: text_contains={text_contains}, text={text}"
        log_assert(f"FAILED: {error_msg}", passed=False)
        raise AssertionError(error_msg)
    else:
        text_display = text_contains or text or resource_id or "element"
        log_assert(f"Element does not exist: {text_display}", passed=True)
        return True


def assert_text_in_dump(text: str, timeout: float = 5.0, message: str = None):
    """
    Assert that text exists in current UI dump.
    
    Args:
        text: Text to search for
        timeout: Timeout in seconds
        message: Custom error message
        
    Raises:
        AssertionError: If text not found
    """
    return assert_element_exists(text_contains=text, timeout=timeout, message=message)


def assert_text_not_in_dump(text: str, timeout: float = 3.0, message: str = None):
    """
    Assert that text does NOT exist in current UI dump.
    
    Args:
        text: Text to search for
        timeout: Timeout in seconds
        message: Custom error message
        
    Raises:
        AssertionError: If text is found
    """
    return assert_element_not_exists(text_contains=text, timeout=timeout, message=message)

