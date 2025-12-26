"""Test case: Điền form và input text."""
from commons.setup import setup_app
from commons.helpers import execute_steps
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_form_input():
    """
    Test case: Điền form và input text.
    
    Trường hợp sử dụng:
    - Điền text vào input field
    - Chọn từ dropdown
    - Chọn date/time
    - Submit form
    """
    log_section("TEST: Form Input")
    
    try:
        setup_app()
        
        # Navigate đến form
        steps = [
            "Khám phá",
            "Hậu mãi VinFast",
            "Đặt lịch dịch vụ",
            ("Đặt lịch dịch vụ", 1),
            "Bảo dưỡng",
            "Tiếp theo",
        ]
        execute_steps(steps)
        
        # Điền form
        steps = [
            # Chọn tỉnh/thành phố
            "Tỉnh/Thành phố",
            "Đà Nẵng",
            "Chọn tỉnh",
            
            # Chọn xưởng dịch vụ
            "Chọn xưởng dịch vụ",
            "VinFast Hải Châu",
            
            # Chọn ngày
            "Chọn ngày",
            "31",
            "Lưu thay đổi",
            
            # Chọn giờ
            "11:00",
            
            # Submit
            "Tiếp",
        ]
        execute_steps(steps)
        
        # Assertion: Validate form submission
        log_info("Validating test result...")
        # After form submission, should see confirmation or next step
        assert_text_in_dump("Tiếp", timeout=5.0,
                           message="Test FAILED: Form submission not successful")
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_form_input()

