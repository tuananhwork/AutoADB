"""Test case: Scroll để tìm element không hiển thị trên màn hình."""
from commons.setup import setup_app
from commons.helpers import execute_steps, swipe, sleep
from core.waiter import Wait


def test_scroll():
    """
    Test case: Scroll để tìm element không hiển thị.
    
    Trường hợp sử dụng:
    - Element nằm ngoài màn hình hiện tại
    - Cần scroll để element xuất hiện
    - Kết hợp swipe + wait để tìm element
    """
    print("=" * 60)
    print("TEST: Scroll to Find Element")
    print("=" * 60)
    
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
        print(f"\n[SCROLL] Attempt {i+1}/{max_scrolls}")
        
        try:
            # Tìm element
            element = Wait(timeout=3).until_element(text_contains="Đặt lịch dịch vụ")
            print(f"[SCROLL] ✓ Element found after {i+1} scrolls")
            element.click()
            found = True
            break
        except:
            # Chưa thấy, scroll tiếp
            print(f"[SCROLL] ✗ Element not found, scrolling...")
            swipe(540, 1500, 540, 500, duration=500)  # Swipe lên
            sleep(0.5)
    
    if not found:
        print("[SCROLL] ✗ Element not found after max scrolls")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_scroll()

