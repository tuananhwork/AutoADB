"""Example test flow."""
from commons.setup import setup_app
from commons.helpers import execute_steps


def test_dump_flow():
    """Test flow: open app and navigate."""
    print("=" * 60)
    print("STARTING TEST FLOW")
    print("=" * 60)
    
    # Common setup
    setup_app()
    
    # Navigation steps - format options:
    # - Simple: "text_contains"
    # - With nth: ("text_contains", nth)
    # - Full: ("text_contains", nth, wait_after)
    # Step numbers are auto-generated
    steps = [
        "Khám phá",
        "Hậu mãi VinFast",
        ("Đặt lịch dịch vụ", 0),
        ("Đặt lịch dịch vụ", 1),
        "Bảo dưỡng",
        "Tiếp theo",
        "Tỉnh/Thành phố",
        "Đà Nẵng",
        "Chọn tỉnh",
        "Chọn xưởng dịch vụ",
        "VinFast Hải Châu",
        ("Chọn xưởng dịch vụ", 2),
        "Chọn ngày",
        "31",
        "Lưu thay đổi",
        "11:00",
        "Tiếp",
    ]
    
    execute_steps(steps)
    
    print("\n" + "=" * 60)
    print("TEST FLOW COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_dump_flow()

