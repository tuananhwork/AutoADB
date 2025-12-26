"""Test case: Custom timeout cho từng step."""
from commons.setup import setup_app
from core.waiter import Wait
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_custom_timeout():
    """
    Test case: Sử dụng timeout khác nhau cho từng step.
    
    Trường hợp sử dụng:
    - Step nhanh: timeout ngắn
    - Step chậm (network, loading): timeout dài
    - Tối ưu thời gian chạy test
    """
    log_section("TEST: Custom Timeout per Step")
    
    try:
        setup_app()
        
        # Step nhanh - timeout ngắn
        log_info("Fast step with short timeout...")
        element = Wait(timeout=5).until_element(text_contains="Khám phá")
        element.click()
        
        # Step bình thường - timeout mặc định
        log_info("Normal step with default timeout...")
        element = Wait(timeout=15).until_element(text_contains="Hậu mãi VinFast")
        element.click()
        
        # Step chậm - timeout dài (ví dụ: loading data)
        log_info("Slow step with long timeout...")
        element = Wait(timeout=30).until_element(text_contains="Đặt lịch dịch vụ")
        element.click()
        
        # Step với nth element
        log_info("Waiting for nth element...")
        element = Wait(timeout=30).until_element(text_contains="Đặt lịch dịch vụ", nth=1)
        element.click()
        
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
    test_custom_timeout()
