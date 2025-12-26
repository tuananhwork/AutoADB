"""Test case: Xử lý nhiều element cùng text với nth parameter."""
from commons.setup import setup_app
from commons.helpers import execute_steps
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_nth_element():
    """
    Test case: Xử lý khi có nhiều element cùng text.
    
    Trường hợp sử dụng:
    - Trang có nhiều button cùng text "Đặt lịch dịch vụ"
    - Cần chọn element thứ 2, thứ 3...
    - Sử dụng nth parameter (0-based)
    """
    log_section("TEST: Multiple Elements with Same Text")
    
    try:
        setup_app()
        
        steps = [
            "Khám phá",
            "Hậu mãi VinFast",
            
            # Element đầu tiên (nth=0, mặc định)
            "Đặt lịch dịch vụ",
            
            # Element thứ 2 (nth=1)
            ("Đặt lịch dịch vụ", 1),
            
            "Bảo dưỡng",
        ]
        
        execute_steps(steps)
        
        # Assertion: Validate test result
        log_info("Validating test result...")
        assert_text_in_dump("Bảo dưỡng", timeout=5.0,
                           message="Test FAILED: Expected 'Bảo dưỡng' not found")
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_nth_element()

