"""UI dump and screenshot."""
import os
import time
from datetime import datetime
from typing import Tuple
from core import adb
from config import settings


def dump_ui(prefix: str = "dump") -> Tuple[str, str]:
    """
    Dump UI XML and take screenshot.
    
    Args:
        prefix: Prefix for file names
        
    Returns:
        Tuple of (xml_path, screenshot_path)
    """
    # Create directories if needed
    os.makedirs(settings.DUMP_DIR, exist_ok=True)
    os.makedirs(settings.SCREENSHOT_DIR, exist_ok=True)
    
    # Generate timestamp with microseconds
    now = datetime.now()
    timestamp = f"{now.strftime('%Y%m%d_%H%M%S')}_{int(time.time() * 1000000) % 1000000}"
    
    # Remote paths
    remote_xml = f"/sdcard/ui_dump_{timestamp}.xml"
    remote_screenshot = f"/sdcard/screenshot_{timestamp}.png"
    
    # Local paths
    xml_filename = f"{prefix}_{timestamp}.xml"
    screenshot_filename = f"{prefix}_{timestamp}.png"
    xml_path = os.path.join(settings.DUMP_DIR, xml_filename)
    screenshot_path = os.path.join(settings.SCREENSHOT_DIR, screenshot_filename)
    
    # Dump UI XML
    print(f"[DUMP] Dumping UI XML...")
    adb.run(f"shell uiautomator dump {remote_xml}")
    
    # Take screenshot
    print(f"[DUMP] Taking screenshot...")
    adb.run(f"shell screencap -p {remote_screenshot}")
    
    # Pull files
    print(f"[DUMP] Pulling files...")
    adb.run(f"pull {remote_xml} {xml_path}")
    adb.run(f"pull {remote_screenshot} {screenshot_path}")
    
    # Clean up remote files
    adb.run(f"shell rm {remote_xml}")
    adb.run(f"shell rm {remote_screenshot}")
    
    print(f"[DUMP] Dump completed: {xml_filename}")
    return xml_path, screenshot_path

