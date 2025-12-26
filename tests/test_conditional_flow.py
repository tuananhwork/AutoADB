"""Test case: Conditional flow - xử lý logic điều kiện."""
from commons.setup import setup_app
from commons.helpers import execute_steps
from core.waiter import Wait
from core.exceptions import TimeoutException
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_conditional_flow():
    """
    Test case: Xử lý flow có điều kiện.
    
    Trường hợp sử dụng:
    - Có popup/dialog xuất hiện không đều
    - Cần kiểm tra element có tồn tại không
    - Xử lý các trường hợp khác nhau
    - Skip step nếu không cần thiết
    """
    log_section("TEST: Conditional Flow")
    
    try:
        setup_app()
        
        # Navigate vào app
        steps = [
            "Khám phá",
            "Hậu mãi VinFast",
        ]
        execute_steps(steps)
        
        # Kiểm tra và xử lý popup nếu có
        log_info("Checking for popup...")
        try:
            # Thử tìm popup với timeout ngắn
            popup = Wait(timeout=2).until_element(text_contains="Đóng")
            log_info("Popup found, closing it...")
            popup.click()
        except TimeoutException:
            log_info("No popup found, continuing...")
        
        # Tiếp tục flow chính
        steps = [
            "Đặt lịch dịch vụ",
            ("Đặt lịch dịch vụ", 1),
            "Bảo dưỡng",
        ]
        execute_steps(steps)
        
        # Kiểm tra và xử lý permission dialog
        log_info("Checking for permission dialog...")
        try:
            allow_button = Wait(timeout=3).until_element(text_contains="Cho phép")
            log_info("Permission dialog found, allowing...")
            allow_button.click()
        except TimeoutException:
            log_info("No permission dialog, continuing...")
        
        # Flow tiếp theo
        steps = [
            "Tiếp theo",
        ]
        execute_steps(steps)
        
        # Assertion: Validate test result
        log_info("Validating test result...")
        assert_text_in_dump("Tỉnh/Thành phố", timeout=5.0,
                           message="Test FAILED: Expected 'Tỉnh/Thành phố' not found")
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_conditional_flow()

