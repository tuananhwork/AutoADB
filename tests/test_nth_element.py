"""Test case: Xử lý nhiều element cùng text với nth parameter."""
from commons.setup import setup_app
from commons.helpers import execute_steps


def test_nth_element():
    """
    Test case: Xử lý khi có nhiều element cùng text.
    
    Trường hợp sử dụng:
    - Trang có nhiều button cùng text "Đặt lịch dịch vụ"
    - Cần chọn element thứ 2, thứ 3...
    - Sử dụng nth parameter (0-based)
    """
    print("=" * 60)
    print("TEST: Multiple Elements with Same Text")
    print("=" * 60)
    
    setup_app()
    
    steps = [
        "Khám phá",
        "Hậu mãi VinFast",
        
        # Element đầu tiên (nth=0, mặc định)
        ("Đặt lịch dịch vụ", 0),
        
        # Element thứ 2 (nth=1)
        ("Đặt lịch dịch vụ", 1),
        
        # Element thứ 3 (nth=2)
        ("Đặt lịch dịch vụ", 2),
        
        "Bảo dưỡng",
    ]
    
    execute_steps(steps)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_nth_element()

