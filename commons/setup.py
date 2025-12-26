"""Common setup functions for tests."""
import time
from core import app
from commons.logger import log_setup, log_teardown


def setup_app(package: str = None, stabilize_delay: float = 2.0):
    """
    Common setup: stop and start app.
    
    Args:
        package: Package name (uses config default if None)
        stabilize_delay: Seconds to wait after app starts (default: 2.0)
    """
    log_setup("Stop app")
    app.stop_app()
    
    log_setup("Start app")
    app.start_app(package)
    
    if stabilize_delay > 0:
        log_setup(f"Waiting {stabilize_delay}s for app to stabilize...")
        time.sleep(stabilize_delay)
    
    log_setup("Setup completed")


def teardown_app(package: str = None):
    """
    Common teardown: stop app.
    
    Args:
        package: Package name (uses config default if None)
    """
    log_teardown("Stop app")
    app.stop_app()
    log_teardown("Teardown completed")

