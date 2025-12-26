"""Test case: Sử dụng key events (BACK, HOME, etc.)."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, key, sleep


def test_key_events():
    """
    Test case: Sử dụng các key events.
    
    Trường hợp sử dụng:
    - Nhấn BACK button để quay lại
    - Nhấn HOME để về home screen
    - Điều hướng bằng hardware keys
    - Xử lý dialog/popup bằng BACK
    """
    print("=" * 60)
    print("TEST: Key Events")
    print("=" * 60)
    
    setup_app()
    
    steps = [
        # Navigate vào app
        touch("Khám phá"),
        touch("Hậu mãi VinFast"),
        
        # Nhấn BACK để quay lại
        key(4),  # BACK button
        sleep(1.0),
        
        # Navigate tiếp
        touch("Đặt lịch dịch vụ"),
        
        # Nhấn BACK lần nữa
        key(4),
        sleep(1.0),
        
        # Có thể dùng dict format với description
        {"action": "key", "code": 3, "desc": "[STEP] Press HOME", "wait_after": 1.0},
        
        # Key codes phổ biến:
        # 3 = HOME
        # 4 = BACK
        # 24 = VOLUME_UP
        # 25 = VOLUME_DOWN
        # 66 = ENTER
    ]
    
    execute_steps(steps)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_key_events()

