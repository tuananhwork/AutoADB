"""Test case: Workflow phức tạp kết hợp nhiều loại action."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, tap, swipe, key, sleep


def test_mixed_workflow():
    """
    Test case: Workflow phức tạp kết hợp nhiều action types.
    
    Trường hợp sử dụng:
    - Test flow thực tế với nhiều bước
    - Kết hợp touch, tap, swipe, key
    - Xử lý các tình huống phức tạp
    - Real-world scenario
    """
    print("=" * 60)
    print("TEST: Complex Mixed Workflow")
    print("=" * 60)
    
    setup_app()
    
    steps = [
        # Bước 1: Navigate vào menu
        touch("Khám phá"),
        touch("Hậu mãi VinFast"),
        
        # Bước 2: Chọn dịch vụ (có nhiều element cùng text)
        ("Đặt lịch dịch vụ", 0),
        touch("Bảo dưỡng"),
        
        # Bước 3: Scroll để tìm option
        swipe(540, 1500, 540, 500, duration=500),
        sleep(1.0),  # Đợi UI ổn định
        
        # Bước 4: Tap tại vị trí cụ thể (nếu element không có text)
        tap(540, 1200),
        
        # Bước 5: Điền form
        touch("Tỉnh/Thành phố"),
        touch("Đà Nẵng"),
        touch("Chọn tỉnh"),
        
        # Bước 6: Scroll để tìm xưởng dịch vụ
        swipe(540, 1500, 540, 500, duration=500),
        touch("Chọn xưởng dịch vụ"),
        touch("VinFast Hải Châu"),
        
        # Bước 7: Chọn ngày giờ
        touch("Chọn ngày"),
        touch("31"),
        touch("Lưu thay đổi"),
        touch("11:00"),
        
        # Bước 8: Submit
        touch("Tiếp"),
        
        # Bước 9: Nếu có popup, nhấn BACK
        sleep(2.0),  # Đợi popup xuất hiện
        key(4),  # BACK để đóng popup nếu có
        
        # Bước 10: Xác nhận
        touch("Xác nhận"),
    ]
    
    execute_steps(steps)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_mixed_workflow()

