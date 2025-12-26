"""Common helper functions for tests."""
import time
from core.waiter import Wait
from core import dump, device
from config import settings


# Helper functions for creating action dicts (optional, for convenience)
def touch(text: str, nth: int = 0, wait_after: float = 1.0, timeout: float = 15.0, desc: str = None):
    """Create touch action dict."""
    return {"action": "touch", "text": text, "nth": nth, "wait_after": wait_after, "timeout": timeout, "desc": desc}


def tap(x: int, y: int, wait_after: float = 1.0, desc: str = None):
    """Create tap action dict."""
    return {"action": "tap", "x": x, "y": y, "wait_after": wait_after, "desc": desc}


def swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300, wait_after: float = 1.0, desc: str = None):
    """Create swipe action dict."""
    return {"action": "swipe", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "duration": duration, "wait_after": wait_after, "desc": desc}


def key(code: int, wait_after: float = 1.0, desc: str = None):
    """Create key event action dict."""
    return {"action": "key", "code": code, "wait_after": wait_after, "desc": desc}


def sleep(duration: float, desc: str = None):
    """Create sleep action dict."""
    return {"action": "sleep", "duration": duration, "desc": desc}


# Assertion helper functions
def assert_exists(text: str = None, text_contains: str = None, resource_id: str = None,
                 class_name: str = None, nth: int = 0, timeout: float = 5.0, message: str = None):
    """Create assert exists action dict."""
    return {"assert": "exists", "text": text, "text_contains": text_contains,
           "resource_id": resource_id, "class_name": class_name, "nth": nth,
           "timeout": timeout, "message": message}


def assert_not_exists(text: str = None, text_contains: str = None, resource_id: str = None,
                     class_name: str = None, timeout: float = 3.0, message: str = None):
    """Create assert not exists action dict."""
    return {"assert": "not_exists", "text": text, "text_contains": text_contains,
           "resource_id": resource_id, "class_name": class_name,
           "timeout": timeout, "message": message}


def click_element(description: str, text_contains: str = None, 
                  text: str = None, nth: int = 0, wait_after: float = 1.0, 
                  timeout: float = 15.0, dump_after: bool = None):
    """
    Helper function to click element with logging.
    
    Args:
        description: Step description
        text_contains: Text substring to match
        text: Exact text to match
        nth: Index of element (0-based)
        wait_after: Seconds to wait after click
        timeout: Timeout in seconds
        dump_after: Dump screenshot/XML after click (None = use config default)
    """
    from commons.logger import log_info, log_dump, log_error
    log_info(description)
    try:
        Wait(timeout=timeout).until_element(text_contains=text_contains, text=text, nth=nth).click()
        
        # Dump after successful click if enabled
        should_dump = dump_after if dump_after is not None else settings.DUMP_ON_EACH_STEP
        if should_dump:
            step_name = description.lower().replace(" ", "_").replace("'", "").replace("[", "").replace("]", "")
            xml_path, screenshot_path = dump.dump_ui(f"step_{step_name}", screenshot=True)
            log_dump(f"Step completed - XML: {xml_path}, Screenshot: {screenshot_path}")
        
        if wait_after > 0:
            time.sleep(wait_after)
    except Exception as e:
        # Always dump on error for debugging
        if settings.DUMP_ON_ERROR:
            step_name = description.lower().replace(" ", "_").replace("'", "").replace("[", "").replace("]", "")
            xml_path, screenshot_path = dump.dump_ui(f"error_{step_name}", screenshot=True)
            log_error(f"Error occurred - XML: {xml_path}, Screenshot: {screenshot_path}")
        raise


def assert_action(action_dict: dict, step_num: int):
    """
    Execute assertion action.
    
    Args:
        action_dict: Dict with assertion type and parameters
        step_num: Step number for logging
    """
    from commons.assertions import assert_element_exists, assert_element_not_exists, assert_text_in_dump, assert_text_not_in_dump
    
    assert_type = action_dict.get("assert", "exists")  # Default to "exists"
    
    if assert_type == "exists" or assert_type is None:
        assert_element_exists(
            text_contains=action_dict.get("text_contains") or action_dict.get("text"),
            text=action_dict.get("text"),
            resource_id=action_dict.get("resource_id"),
            class_name=action_dict.get("class_name"),
            nth=action_dict.get("nth", 0),
            timeout=action_dict.get("timeout", 5.0),
            message=action_dict.get("message")
        )
    elif assert_type == "not_exists":
        assert_element_not_exists(
            text_contains=action_dict.get("text_contains") or action_dict.get("text"),
            text=action_dict.get("text"),
            resource_id=action_dict.get("resource_id"),
            class_name=action_dict.get("class_name"),
            timeout=action_dict.get("timeout", 3.0),
            message=action_dict.get("message")
        )
    elif assert_type == "text_in_dump":
        assert_text_in_dump(
            text=action_dict.get("text") or action_dict.get("text_contains"),
            timeout=action_dict.get("timeout", 5.0),
            message=action_dict.get("message")
        )
    elif assert_type == "text_not_in_dump":
        assert_text_not_in_dump(
            text=action_dict.get("text") or action_dict.get("text_contains"),
            timeout=action_dict.get("timeout", 3.0),
            message=action_dict.get("message")
        )
    else:
        raise ValueError(f"Unknown assert type: {assert_type}")


def execute_action(action_dict: dict, step_num: int, wait_after: float = 1.0):
    """
    Execute a single action from action dict.
    
    Args:
        action_dict: Dict with action type and parameters
        step_num: Step number for logging
        wait_after: Seconds to wait after action
    """
    action_type = action_dict.get("action", "touch")  # Default to touch for backward compatibility
    
    try:
        if action_type == "touch" or action_type is None:
            # Touch by text
            text = action_dict.get("text") or action_dict.get("text_contains")
            nth = action_dict.get("nth", 0)
            timeout = action_dict.get("timeout", 15.0)
            desc = action_dict.get("desc") or f"[STEP {step_num}] Touch '{text}'" + (f" (nth={nth})" if nth > 0 else "")
            click_element(desc, text_contains=text, nth=nth, wait_after=wait_after, timeout=timeout)
            
        elif action_type == "tap":
            # Tap at coordinates
            from commons.logger import log_info
            x = action_dict["x"]
            y = action_dict["y"]
            desc = action_dict.get("desc") or f"[STEP {step_num}] Tap at ({x}, {y})"
            log_info(desc)
            device.tap(x, y)
            if wait_after > 0:
                time.sleep(wait_after)
                
        elif action_type == "swipe":
            # Swipe from (x1, y1) to (x2, y2)
            from commons.logger import log_info
            x1 = action_dict["x1"]
            y1 = action_dict["y1"]
            x2 = action_dict["x2"]
            y2 = action_dict["y2"]
            duration = action_dict.get("duration", 300)
            desc = action_dict.get("desc") or f"[STEP {step_num}] Swipe from ({x1}, {y1}) to ({x2}, {y2})"
            log_info(desc)
            device.swipe(x1, y1, x2, y2, duration)
            if wait_after > 0:
                time.sleep(wait_after)
                
        elif action_type == "key" or action_type == "keyevent":
            # Send key event
            from commons.logger import log_info
            code = action_dict["code"]
            key_names = {3: "HOME", 4: "BACK", 24: "VOLUME_UP", 25: "VOLUME_DOWN", 66: "ENTER"}
            key_name = key_names.get(code, f"KEY_{code}")
            desc = action_dict.get("desc") or f"[STEP {step_num}] Key {key_name} ({code})"
            log_info(desc)
            device.keyevent(code)
            if wait_after > 0:
                time.sleep(wait_after)
                
        elif action_type == "sleep" or action_type == "wait":
            # Sleep/wait
            from commons.logger import log_info
            duration = action_dict.get("duration", wait_after)
            desc = action_dict.get("desc") or f"[STEP {step_num}] Wait {duration}s"
            log_info(desc)
            time.sleep(duration)
            
        else:
            raise ValueError(f"Unknown action type: {action_type}")
            
    except Exception as e:
        if settings.DUMP_ON_ERROR:
            step_name = desc.lower().replace(" ", "_").replace("'", "").replace("[", "").replace("]", "")
            xml_path, screenshot_path = dump.dump_ui(f"error_{step_name}")
            print(f"[DUMP] Error occurred - XML: {xml_path}, Screenshot: {screenshot_path}")
        raise


def execute_steps(steps: list, start_step_num: int = 1):
    """
    Execute a list of steps with mixed action types.
    
    Args:
        steps: List of steps - can be:
               # Simple text (backward compatible):
               - "text_contains" or ("text_contains", nth) or ("text_contains", nth, wait_after)
               
               # Action dict format:
               - {"action": "touch", "text": "Khám phá", "nth": 0, "wait_after": 1.0}
               - {"action": "tap", "x": 100, "y": 200}
               - {"action": "swipe", "x1": 100, "y1": 200, "x2": 300, "y2": 400}
               - {"action": "key", "code": 4}  # BACK key
               - {"action": "sleep", "duration": 2.0}
        start_step_num: Starting step number for logging
    """
    for i, step_info in enumerate(steps, start=start_step_num):
        # Handle dict format (new action system)
        if isinstance(step_info, dict):
            # Check if it's an assertion
            if "assert" in step_info:
                assert_action(step_info, i)
            else:
                wait_after = step_info.get("wait_after", 1.0)
                execute_action(step_info, i, wait_after)
            continue
        
        # Handle string/tuple format (backward compatible)
        if isinstance(step_info, str):
            # Simple string: "text_contains"
            text = step_info
            nth = 0
            wait_after = 1.0
            desc = f"[STEP {i}] Touch '{text}'"
        elif len(step_info) == 1:
            # Tuple with 1 element: ("text_contains",)
            text = step_info[0]
            nth = 0
            wait_after = 1.0
            desc = f"[STEP {i}] Touch '{text}'"
        elif len(step_info) == 2:
            # Check if first element is description (legacy format) or text_contains
            if isinstance(step_info[0], str) and step_info[0].startswith("[STEP"):
                # Legacy format: (description, "text_contains")
                desc = step_info[0]
                text = step_info[1]
                nth = 0
                wait_after = 1.0
            else:
                # New format: ("text_contains", nth)
                text = step_info[0]
                nth = step_info[1]
                wait_after = 1.0
                desc = f"[STEP {i}] Touch '{text}'" + (f" (nth={nth})" if nth > 0 else "")
        elif len(step_info) == 3:
            # Check if first element is description (legacy format)
            if isinstance(step_info[0], str) and step_info[0].startswith("[STEP"):
                # Legacy format: (description, "text_contains", nth)
                desc = step_info[0]
                text = step_info[1]
                nth = step_info[2]
                wait_after = 1.0
            else:
                # New format: ("text_contains", nth, wait_after)
                text = step_info[0]
                nth = step_info[1]
                wait_after = step_info[2]
                desc = f"[STEP {i}] Touch '{text}'" + (f" (nth={nth})" if nth > 0 else "")
        else:
            # Legacy format: (description, "text_contains", nth, wait_after)
            desc = step_info[0]
            text = step_info[1]
            nth = step_info[2] if len(step_info) > 2 else 0
            wait_after = step_info[3] if len(step_info) > 3 else 1.0
        
        click_element(desc, text_contains=text, nth=nth, wait_after=wait_after)

