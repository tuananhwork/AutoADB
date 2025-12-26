"""Test case: Sử dụng key events (BACK, HOME, etc.)."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, key, sleep
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_key_events():
    """
    Test case: Sử dụng các key events.
    
    Trường hợp sử dụng:
    - Nhấn BACK button để quay lại
    - Nhấn HOME để về home screen
    - Điều hướng bằng hardware keys
    - Xử lý dialog/popup bằng BACK
    """
    log_section("TEST: Key Events")
    
    try:
        setup_app()
        
        steps = [
            # Navigate vào app
            touch("Khám phá"),
            touch("Hậu mãi VinFast"),
            
            # Nhấn BACK để quay lại
            key(4),  # BACK button
            sleep(1.0),
            
            # Navigate tiếp
            touch("Đặt lịch dịch vụ"),
            touch("Đặt lịch dịch vụ", 1),
            
            # Nhấn BACK lần nữa
            key(4),
            sleep(1.0),
            
            # Navigate lại để validate
            touch("Khám phá"),
        ]
        
        execute_steps(steps)
        
        # Assertion: Validate test result
        log_info("Validating test result...")
        assert_text_in_dump("Khám phá", timeout=5.0,
                           message="Test FAILED: Expected 'Khám phá' not found after key events")
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_key_events()

