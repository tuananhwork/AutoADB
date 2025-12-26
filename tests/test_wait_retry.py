"""Test case: Wait và retry mechanism."""
from commons.setup import setup_app
from core.waiter import Wait
from core.exceptions import TimeoutException


def test_wait_retry():
    """
    Test case: Sử dụng wait và retry mechanism.
    
    Trường hợp sử dụng:
    - Element load chậm, cần đợi
    - Network request đang xử lý
    - Animation đang chạy
    - Custom timeout và interval
    """
    print("=" * 60)
    print("TEST: Wait and Retry")
    print("=" * 60)
    
    setup_app()
    
    # Wait với timeout mặc định (15s)
    print("\n[WAIT] Waiting for element with default timeout...")
    element = Wait().until_element(text_contains="Khám phá")
    element.click()
    
    # Wait với timeout dài hơn
    print("\n[WAIT] Waiting with longer timeout (30s)...")
    element = Wait(timeout=30).until_element(text_contains="Slow loading button")
    element.click()
    
    # Wait với interval ngắn hơn (polling nhanh hơn)
    print("\n[WAIT] Waiting with shorter interval (0.5s)...")
    element = Wait(timeout=15, interval=0.5).until_element(text_contains="Button")
    element.click()
    
    # Wait với nth element
    print("\n[WAIT] Waiting for nth element...")
    element = Wait(timeout=15).until_element(text_contains="Đặt lịch dịch vụ", nth=1)
    element.click()
    
    # Xử lý timeout exception
    try:
        print("\n[WAIT] Waiting for non-existent element (will timeout)...")
        element = Wait(timeout=5).until_element(text_contains="NonExistentButton")
    except TimeoutException as e:
        print(f"[WAIT] Expected timeout: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_wait_retry()

