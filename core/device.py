"""Device interaction methods."""
from core import adb


def tap(x: int, y: int) -> None:
    """
    Tap at coordinates.
    
    Args:
        x: X coordinate
        y: Y coordinate
    """
    adb.run(f"shell input tap {x} {y}")


def swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> None:
    """
    Swipe from (x1, y1) to (x2, y2).
    
    Args:
        x1: Start X coordinate
        y1: Start Y coordinate
        x2: End X coordinate
        y2: End Y coordinate
        duration: Swipe duration in milliseconds (default: 300)
    """
    adb.run(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")


def keyevent(code: int) -> None:
    """
    Send key event.
    
    Args:
        code: Key code (e.g., 4 for BACK, 3 for HOME)
    """
    adb.run(f"shell input keyevent {code}")

