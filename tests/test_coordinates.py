"""Test case: Tap và swipe theo tọa độ."""
from commons.setup import setup_app
from commons.helpers import execute_steps, tap, swipe
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_coordinates():
    """
    Test case: Sử dụng tap và swipe theo tọa độ.
    
    Trường hợp sử dụng:
    - Element không có text hoặc text không ổn định
    - Cần tap tại vị trí cố định
    - Cần swipe để scroll/navigate
    - Element là image/icon không có text
    """
    log_section("TEST: Tap and Swipe by Coordinates")
    
    try:
        setup_app()
        
        steps = [
            # Touch by text
            "Khám phá",
            
            # Tap tại tọa độ cụ thể (ví dụ: center screen)
            tap(540, 1200),
            
            # Swipe lên để scroll
            swipe(540, 1500, 540, 500, duration=500),
            
            # Swipe xuống
            swipe(540, 500, 540, 1500, duration=500),
            
            # Swipe sang trái
            swipe(900, 1200, 100, 1200, duration=300),
            
            # Swipe sang phải
            swipe(100, 1200, 900, 1200, duration=300),
            
            # Navigate back to test area
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
    test_coordinates()

