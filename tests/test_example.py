"""Example test using common setup."""
from commons.setup import setup_app
from commons.helpers import execute_steps
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_example_flow():
    """Example test flow using common setup."""
    log_section("STARTING EXAMPLE TEST")
    
    try:
        setup_app()
        
        # Test-specific steps
        steps = [
            "Khám phá",
            "Hậu mãi VinFast",
        ]
        
        execute_steps(steps)
        
        # Assertion: Validate test result
        log_info("Validating test result...")
        assert_text_in_dump("Hậu mãi VinFast", timeout=5.0,
                           message="Test FAILED: Expected 'Hậu mãi VinFast' not found")
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_example_flow()

