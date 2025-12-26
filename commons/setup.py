"""Common setup functions for tests."""
import time
from core import app


def setup_app(package: str = None, stabilize_delay: float = 2.0):
    """
    Common setup: stop and start app.
    
    Args:
        package: Package name (uses config default if None)
        stabilize_delay: Seconds to wait after app starts (default: 2.0)
    """
    print("\n[SETUP] Stop app")
    app.stop_app()
    
    print("\n[SETUP] Start app")
    app.start_app(package)
    
    if stabilize_delay > 0:
        print(f"\n[SETUP] Waiting {stabilize_delay}s for app to stabilize...")
        time.sleep(stabilize_delay)
    
    print("[SETUP] Setup completed")


def teardown_app(package: str = None):
    """
    Common teardown: stop app.
    
    Args:
        package: Package name (uses config default if None)
    """
    print("\n[TEARDOWN] Stop app")
    app.stop_app()
    print("[TEARDOWN] Teardown completed")

