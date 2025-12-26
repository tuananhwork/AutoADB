"""Colored logging utility."""
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Auto reset color after each print
    COLORAMA_AVAILABLE = True
except ImportError:
    # Fallback nếu không có colorama
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        BLUE = ""
        CYAN = ""
        MAGENTA = ""
        RESET = ""
    class Style:
        BRIGHT = ""
        RESET_ALL = ""
    COLORAMA_AVAILABLE = False


def log_step(step_num: int, description: str, status: str = "info"):
    """
    Log step with color.
    
    Args:
        step_num: Step number
        description: Step description
        status: "info", "success", "error", "warning"
    """
    if status == "success":
        color = Fore.GREEN
        prefix = "[PASS]"
    elif status == "error":
        color = Fore.RED
        prefix = "[FAIL]"
    elif status == "warning":
        color = Fore.YELLOW
        prefix = "[WARN]"
    else:
        color = Fore.CYAN
        prefix = "[INFO]"
    
    print(f"{color}{prefix} [STEP {step_num}] {description}{Fore.RESET}")


def log_info(message: str):
    """Log info message."""
    print(f"{Fore.CYAN}[INFO] {message}{Fore.RESET}")


def log_success(message: str):
    """Log success message."""
    print(f"{Fore.GREEN}[PASS] {message}{Fore.RESET}")


def log_error(message: str):
    """Log error message."""
    print(f"{Fore.RED}[FAIL] {message}{Fore.RESET}")


def log_warning(message: str):
    """Log warning message."""
    print(f"{Fore.YELLOW}[WARN] {message}{Fore.RESET}")


def log_section(title: str, char: str = "="):
    """Log section header."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{char * 60}{Fore.RESET}")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{title}{Fore.RESET}")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{char * 60}{Fore.RESET}")


def log_app(message: str):
    """Log app-related message."""
    print(f"{Fore.BLUE}[APP] {message}{Fore.RESET}")


def log_dump(message: str):
    """Log dump-related message."""
    print(f"{Fore.CYAN}[DUMP] {message}{Fore.RESET}")


def log_wait(message: str):
    """Log wait-related message."""
    print(f"{Fore.YELLOW}[WAIT] {message}{Fore.RESET}")


def log_click(message: str):
    """Log click-related message."""
    print(f"{Fore.GREEN}[CLICK] {message}{Fore.RESET}")


def log_assert(message: str, passed: bool = True):
    """Log assertion message."""
    if passed:
        print(f"{Fore.GREEN}[ASSERT] [PASS] {message}{Fore.RESET}")
    else:
        print(f"{Fore.RED}[ASSERT] [FAIL] {message}{Fore.RESET}")


def log_setup(message: str):
    """Log setup-related message."""
    print(f"{Fore.BLUE}[SETUP] {message}{Fore.RESET}")


def log_teardown(message: str):
    """Log teardown-related message."""
    print(f"{Fore.BLUE}[TEARDOWN] {message}{Fore.RESET}")

