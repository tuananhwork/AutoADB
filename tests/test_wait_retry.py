"""Test case: Wait và retry mechanism."""
from commons.setup import setup_app
from core.waiter import Wait
from core.exceptions import TimeoutException
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_wait_retry():
    """
    Test case: Sử dụng wait và retry mechanism.
    
    Trường hợp sử dụng:
    - Element load chậm, cần đợi
    - Network request đang xử lý
    - Animation đang chạy
    - Custom timeout và interval
    """
    log_section("TEST: Wait and Retry")
    
    try:
        setup_app()
        
        # Wait với timeout mặc định (15s)
        log_info("Waiting for element with default timeout...")
        element = Wait().until_element(text_contains="Khám phá")
        element.click()
        
        # Wait với timeout dài hơn
        log_info("Waiting with longer timeout...")
        element = Wait(timeout=30).until_element(text_contains="Hậu mãi VinFast")
        element.click()
        
        # Wait với interval ngắn hơn (polling nhanh hơn)
        log_info("Waiting with shorter interval (0.5s)...")
        element = Wait(timeout=15, interval=0.5).until_element(text_contains="Đặt lịch dịch vụ")
        element.click()
        
        # Wait với nth element
        log_info("Waiting for nth element...")
        element = Wait(timeout=15).until_element(text_contains="Đặt lịch dịch vụ", nth=1)
        element.click()
        
        # Xử lý timeout exception (expected behavior)
        try:
            log_info("Waiting for non-existent element (will timeout)...")
            element = Wait(timeout=2).until_element(text_contains="NonExistentButton12345")
        except TimeoutException:
            log_info("Expected timeout occurred - this is correct behavior")
        
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
    test_wait_retry()

