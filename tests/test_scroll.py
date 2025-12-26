"""Test case: Scroll để tìm element không hiển thị trên màn hình."""
from commons.setup import setup_app
from commons.helpers import execute_steps, swipe, sleep
from core.waiter import Wait
from core.exceptions import TimeoutException
from commons.assertions import AssertionError
from commons.logger import log_section, log_info, log_success, log_error


def test_scroll():
    """
    Test case: Scroll để tìm element không hiển thị.
    
    Trường hợp sử dụng:
    - Element nằm ngoài màn hình hiện tại
    - Cần scroll để element xuất hiện
    - Kết hợp swipe + wait để tìm element
    """
    log_section("TEST: Scroll to Find Element")
    
    try:
        setup_app()
        
        # Touch element đầu tiên
        steps = [
            "Khám phá",
            "Hậu mãi VinFast",
        ]
        execute_steps(steps)
        
        # Scroll và tìm element
        max_scrolls = 5
        found = False
        
        for i in range(max_scrolls):
            log_info(f"Scroll attempt {i+1}/{max_scrolls}")
            
            try:
                # Tìm element
                element = Wait(timeout=3).until_element(text_contains="Đặt lịch dịch vụ")
                log_success(f"Element found after {i+1} scrolls")
                element.click()
                found = True
                break
            except TimeoutException:
                # Chưa thấy, scroll tiếp
                log_info("Element not found, scrolling...")
                swipe(540, 1500, 540, 500, duration=500)  # Swipe lên
                sleep(0.5)
        
        # Assertion: Validate element was found
        if not found:
            raise AssertionError("Test FAILED: Element 'Đặt lịch dịch vụ' not found after max scrolls")
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_scroll()

