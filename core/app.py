"""App management."""
import time
from core import adb
from config import app


def start_app(package: str = None) -> None:
    """
    Start app using monkey.
    
    Args:
        package: Package name (uses config default if None)
    """
    pkg = package or app.PACKAGE_NAME
    print(f"[APP] Starting app: {pkg}")
    adb.run(f"shell monkey -p {pkg} -c android.intent.category.LAUNCHER 1")
    print(f"[APP] Waiting {app.LAUNCH_DELAY}s for app to load...")
    time.sleep(app.LAUNCH_DELAY)
    print(f"[APP] App started successfully")


def stop_app(package: str = None) -> None:
    """
    Stop app by force stop.
    
    Args:
        package: Package name (uses config default if None)
    """
    pkg = package or app.PACKAGE_NAME
    print(f"[APP] Stopping app: {pkg}")
    adb.run(f"shell am force-stop {pkg}")
    print(f"[APP] App stopped")

