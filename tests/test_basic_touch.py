"""Test case: Basic touch by text - Trường hợp cơ bản nhất."""
from commons.setup import setup_app
from commons.helpers import execute_steps


def test_basic_touch():
    """
    Test case cơ bản: Touch các element theo text.
    
    Trường hợp sử dụng:
    - Test flow đơn giản, chỉ cần touch theo text
    - Không cần xử lý đặc biệt
    - Format ngắn gọn nhất
    """
    print("=" * 60)
    print("TEST: Basic Touch by Text")
    print("=" * 60)
    
    setup_app()
    
    # Format đơn giản nhất - chỉ cần text
    steps = [
        "Khám phá",
        "Hậu mãi VinFast",
        "Đặt lịch dịch vụ",
        "Bảo dưỡng",
        "Tiếp theo",
    ]
    
    execute_steps(steps)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_basic_touch()

