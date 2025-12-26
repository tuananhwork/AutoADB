"""Test case: Workflow phức tạp kết hợp nhiều loại action."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, tap, swipe, key, sleep
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_mixed_workflow():
    """
    Test case: Workflow phức tạp kết hợp nhiều action types.
    
    Trường hợp sử dụng:
    - Test flow thực tế với nhiều bước
    - Kết hợp touch, tap, swipe, key
    - Xử lý các tình huống phức tạp
    - Real-world scenario
    """
    log_section("TEST: Complex Mixed Workflow")
    
    try:
        setup_app()
        
        steps = [
            # Bước 1: Navigate vào menu
            touch("Khám phá"),
            touch("Hậu mãi VinFast"),
            
            # Bước 2: Chọn dịch vụ (có nhiều element cùng text)
            ("Đặt lịch dịch vụ", 0),
            ("Đặt lịch dịch vụ", 1),
            touch("Bảo dưỡng"),
            
            # Bước 3: Scroll để tìm option
            swipe(540, 1500, 540, 500, duration=500),
            sleep(1.0),  # Đợi UI ổn định
            
            # Bước 4: Điền form
            touch("Tỉnh/Thành phố"),
            touch("Đà Nẵng"),
            touch("Chọn tỉnh"),
            
            # Bước 5: Scroll để tìm xưởng dịch vụ
            swipe(540, 1500, 540, 500, duration=500),
            touch("Chọn xưởng dịch vụ"),
            touch("VinFast Hải Châu"),
            
            # Bước 6: Chọn ngày giờ
            touch("Chọn ngày"),
            touch("31"),
            touch("Lưu thay đổi"),
            touch("11:00"),
            
            # Bước 7: Submit
            touch("Tiếp"),
        ]
        
        execute_steps(steps)
        
        # Assertion: Validate test result
        log_info("Validating test result...")
        # After submitting, should see confirmation or next step
        assert_text_in_dump("Tiếp", timeout=5.0,
                           message="Test FAILED: Expected 'Tiếp' button not found after workflow")
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_mixed_workflow()

