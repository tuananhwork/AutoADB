"""App management."""
import time
from core import adb
from config import app
from commons.logger import log_app


def start_app(package: str = None) -> None:
    """
    Start app using monkey.
    
    Args:
        package: Package name (uses config default if None)
    """
    pkg = package or app.PACKAGE_NAME
    log_app(f"Starting app: {pkg}")
    adb.run(f"shell monkey -p {pkg} -c android.intent.category.LAUNCHER 1")
    log_app(f"Waiting {app.LAUNCH_DELAY}s for app to load...")
    time.sleep(app.LAUNCH_DELAY)
    log_app("App started successfully")


def stop_app(package: str = None) -> None:
    """
    Stop app by force stop.
    
    Args:
        package: Package name (uses config default if None)
    """
    pkg = package or app.PACKAGE_NAME
    log_app(f"Stopping app: {pkg}")
    adb.run(f"shell am force-stop {pkg}")
    log_app("App stopped")

