"""Test case: Điền form và input text."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch
from core.waiter import Wait
from core import device


def test_form_input():
    """
    Test case: Điền form và input text.
    
    Trường hợp sử dụng:
    - Điền text vào input field
    - Chọn từ dropdown
    - Chọn date/time
    - Submit form
    """
    print("=" * 60)
    print("TEST: Form Input")
    print("=" * 60)
    
    setup_app()
    
    # Navigate đến form
    steps = [
        "Khám phá",
        "Hậu mãi VinFast",
        "Đặt lịch dịch vụ",
        "Bảo dưỡng",
        "Tiếp theo",
    ]
    execute_steps(steps)
    
    # Điền form
    steps = [
        # Chọn tỉnh/thành phố
        "Tỉnh/Thành phố",
        "Đà Nẵng",
        "Chọn tỉnh",
        
        # Chọn xưởng dịch vụ
        "Chọn xưởng dịch vụ",
        "VinFast Hải Châu",
        
        # Chọn ngày
        "Chọn ngày",
        "31",
        "Lưu thay đổi",
        
        # Chọn giờ
        "11:00",
        
        # Input text (nếu có field nhập text)
        # Note: Hiện tại framework chưa hỗ trợ input text trực tiếp
        # Có thể dùng adb shell input text "text" nếu cần
        
        # Submit
        "Tiếp",
    ]
    execute_steps(steps)
    
    # Ví dụ input text bằng ADB (nếu cần)
    # device.input_text("Hello World")  # Cần implement trong device.py
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_form_input()

