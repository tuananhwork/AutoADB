"""UI dump and screenshot."""
import os
import time
from datetime import datetime
from typing import Tuple
from core import adb
from config import settings
from commons.logger import log_dump


def dump_ui(prefix: str = "dump", screenshot: bool = True) -> Tuple[str, str]:
    """
    Dump UI XML and optionally take screenshot.
    
    Args:
        prefix: Prefix for file names
        screenshot: Whether to take screenshot (default: True)
        
    Returns:
        Tuple of (xml_path, screenshot_path or empty string)
    """
    # Create directories if needed
    os.makedirs(settings.DUMP_DIR, exist_ok=True)
    if screenshot:
        os.makedirs(settings.SCREENSHOT_DIR, exist_ok=True)
    
    # Generate timestamp with microseconds
    now = datetime.now()
    timestamp = f"{now.strftime('%Y%m%d_%H%M%S')}_{int(time.time() * 1000000) % 1000000}"
    
    # Remote paths
    remote_xml = f"/sdcard/ui_dump_{timestamp}.xml"
    
    # Local paths
    xml_filename = f"{prefix}_{timestamp}.xml"
    xml_path = os.path.join(settings.DUMP_DIR, xml_filename)
    
    # Dump UI XML (always needed for parsing)
    log_dump("Dumping UI XML...")
    adb.run(f"shell uiautomator dump {remote_xml}")
    
    # Pull XML file
    log_dump("Pulling XML file...")
    adb.run(f"pull {remote_xml} {xml_path}")
    
    # Clean up remote XML
    adb.run(f"shell rm {remote_xml}")
    
    screenshot_path = ""
    if screenshot:
        # Take screenshot (optional)
        remote_screenshot = f"/sdcard/screenshot_{timestamp}.png"
        screenshot_filename = f"{prefix}_{timestamp}.png"
        screenshot_path = os.path.join(settings.SCREENSHOT_DIR, screenshot_filename)
        
        log_dump("Taking screenshot...")
        adb.run(f"shell screencap -p {remote_screenshot}")
        
        log_dump("Pulling screenshot...")
        adb.run(f"pull {remote_screenshot} {screenshot_path}")
        
        # Clean up remote screenshot
        adb.run(f"shell rm {remote_screenshot}")
        
        log_dump(f"Dump completed: {xml_filename}, {screenshot_filename}")
    else:
        log_dump(f"Dump completed: {xml_filename} (no screenshot)")
    
    return xml_path, screenshot_path

