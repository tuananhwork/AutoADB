"""Test case: Conditional flow - xử lý logic điều kiện."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch
from core.waiter import Wait
from core.exceptions import TimeoutException


def test_conditional_flow():
    """
    Test case: Xử lý flow có điều kiện.
    
    Trường hợp sử dụng:
    - Có popup/dialog xuất hiện không đều
    - Cần kiểm tra element có tồn tại không
    - Xử lý các trường hợp khác nhau
    - Skip step nếu không cần thiết
    """
    print("=" * 60)
    print("TEST: Conditional Flow")
    print("=" * 60)
    
    setup_app()
    
    # Navigate vào app
    steps = [
        "Khám phá",
        "Hậu mãi VinFast",
    ]
    execute_steps(steps)
    
    # Kiểm tra và xử lý popup nếu có
    print("\n[CONDITIONAL] Checking for popup...")
    try:
        # Thử tìm popup với timeout ngắn
        popup = Wait(timeout=2).until_element(text_contains="Đóng")
        print("[CONDITIONAL] Popup found, closing it...")
        popup.click()
    except TimeoutException:
        print("[CONDITIONAL] No popup found, continuing...")
    
    # Tiếp tục flow chính
    steps = [
        "Đặt lịch dịch vụ",
        "Bảo dưỡng",
    ]
    execute_steps(steps)
    
    # Kiểm tra và xử lý permission dialog
    print("\n[CONDITIONAL] Checking for permission dialog...")
    try:
        allow_button = Wait(timeout=3).until_element(text_contains="Cho phép")
        print("[CONDITIONAL] Permission dialog found, allowing...")
        allow_button.click()
    except TimeoutException:
        print("[CONDITIONAL] No permission dialog, continuing...")
    
    # Flow tiếp theo
    steps = [
        "Tiếp theo",
    ]
    execute_steps(steps)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_conditional_flow()

