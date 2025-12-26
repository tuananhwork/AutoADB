"""Custom exceptions."""


class TimeoutException(Exception):
    """Raised when wait timeout."""
    pass


class ElementNotFoundException(Exception):
    """Raised when element not found."""
    pass

