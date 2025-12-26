"""Test case: Tối ưu performance và tốc độ."""
from commons.setup import setup_app
from commons.helpers import execute_steps
from core.waiter import Wait
from config import settings
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info
import time


def test_performance():
    """
    Test case: Tối ưu performance.
    
    Trường hợp sử dụng:
    - Tắt dump không cần thiết để tăng tốc
    - Sử dụng timeout ngắn cho step nhanh
    - Giảm wait_after khi không cần
    - Batch operations
    """
    log_section("TEST: Performance Optimization")
    
    try:
        # Lưu settings gốc
        original_dump_on_step = settings.DUMP_ON_EACH_STEP
        original_dump_on_wait = settings.DUMP_ON_WAIT
        
        # Tắt dump để tăng tốc
        settings.DUMP_ON_EACH_STEP = False
        settings.DUMP_ON_WAIT = False
        
        try:
            start_time = time.time()
            
            setup_app()
            
            # Sử dụng timeout ngắn cho step nhanh
            log_info("Fast steps with short timeout...")
            element = Wait(timeout=5).until_element(text_contains="Khám phá")
            element.click()
            
            # Giảm wait_after khi không cần
            steps = [
                ("Hậu mãi VinFast", 0, 0.5),  # wait_after = 0.5s thay vì 1.0s
                ("Đặt lịch dịch vụ", 0, 0.5),
                ("Đặt lịch dịch vụ", 1, 0.5),
            ]
            execute_steps(steps)
            
            # Batch operations - không sleep giữa các step liên tiếp
            steps_no_wait = [
                {"action": "touch", "text": "Bảo dưỡng", "wait_after": 0},
                {"action": "touch", "text": "Tiếp theo", "wait_after": 0},
                {"action": "touch", "text": "Tỉnh/Thành phố", "wait_after": 1.0},  # Chỉ wait ở step cuối
            ]
            execute_steps(steps_no_wait)
            
            elapsed = time.time() - start_time
            log_info(f"Total execution time: {elapsed:.2f}s")
            
            # Assertion: Validate test result
            log_info("Validating test result...")
            assert_text_in_dump("Tỉnh/Thành phố", timeout=5.0,
                               message="Test FAILED: Expected 'Tỉnh/Thành phố' not found")
            
        finally:
            # Restore settings
            settings.DUMP_ON_EACH_STEP = original_dump_on_step
            settings.DUMP_ON_WAIT = original_dump_on_wait
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_performance()

