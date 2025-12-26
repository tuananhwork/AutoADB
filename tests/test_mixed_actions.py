"""Example test with mixed actions."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, tap, swipe, key, sleep
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_mixed_actions():
    """Test flow with mixed action types."""
    log_section("STARTING MIXED ACTIONS TEST")
    
    try:
        setup_app()
        
        # Mixed actions - can combine touch, tap, swipe, key, sleep
        steps = [
            # Touch by text (backward compatible - simple format)
            "Khám phá",
            ("Hậu mãi VinFast", 0),
            
            # Using helper functions (cleaner)
            touch("Đặt lịch dịch vụ", nth=0),
            touch("Đặt lịch dịch vụ", nth=1),
            touch("Bảo dưỡng"),
            tap(540, 1200),  # Tap at center
            swipe(540, 1500, 540, 500, duration=500),  # Swipe up
            sleep(1.0),  # Wait 1 second
            touch("Tiếp theo"),
        ]
        
        execute_steps(steps)
        
        # Assertion: Validate test result
        log_info("Validating test result...")
        assert_text_in_dump("Tiếp theo", timeout=5.0,
                           message="Test FAILED: Expected 'Tiếp theo' not found")
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_mixed_actions()

