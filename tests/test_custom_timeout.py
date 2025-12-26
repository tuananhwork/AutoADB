"""Test case: Custom timeout cho từng step."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch
from core.waiter import Wait


def test_custom_timeout():
    """
    Test case: Sử dụng timeout khác nhau cho từng step.
    
    Trường hợp sử dụng:
    - Step nhanh: timeout ngắn
    - Step chậm (network, loading): timeout dài
    - Tối ưu thời gian chạy test
    """
    print("=" * 60)
    print("TEST: Custom Timeout per Step")
    print("=" * 60)
    
    setup_app()
    
    # Step nhanh - timeout ngắn
    print("\n[TIMEOUT] Fast step with short timeout...")
    element = Wait(timeout=5).until_element(text_contains="Khám phá")
    element.click()
    
    # Step bình thường - timeout mặc định
    print("\n[TIMEOUT] Normal step with default timeout...")
    element = Wait(timeout=15).until_element(text_contains="Hậu mãi VinFast")
    element.click()
    
    # Step chậm - timeout dài (ví dụ: loading data)
    print("\n[TIMEOUT] Slow step with long timeout...")
    element = Wait(timeout=30).until_element(text_contains="Đặt lịch dịch vụ")
    element.click()
    
    # Sử dụng trong execute_steps với dict format
    steps = [
        {"action": "touch", "text": "Bảo dưỡng", "timeout": 5},  # Nhanh
        {"action": "touch", "text": "Tiếp theo", "timeout": 15},  # Bình thường
        {"action": "touch", "text": "Xác nhận", "timeout": 30},  # Chậm
    ]
    
    # Note: execute_steps hiện tại chưa hỗ trợ timeout trong dict
    # Có thể dùng Wait trực tiếp như trên
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_custom_timeout()

