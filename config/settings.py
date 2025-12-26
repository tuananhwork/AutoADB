"""Global settings."""
TIMEOUT = 10  # Default timeout in seconds
RETRY_COUNT = 5  # Default retry count
ARTIFACTS_ROOT = "artifacts"
DUMP_DIR = "artifacts/dumps"
SCREENSHOT_DIR = "artifacts/screenshots"
DUMP_DELAY = 0.5  # Delay after dump in seconds

# Dump/Screenshot settings
DUMP_ON_EACH_STEP = False  # Dump after each successful step (for debugging)
DUMP_ON_ERROR = True  # Always dump on error (recommended: True)
DUMP_ON_WAIT = True  # Dump during wait/retry (recommended: True)

