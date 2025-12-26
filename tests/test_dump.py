"""Example test flow."""
from commons.setup import setup_app
from commons.helpers import execute_steps, assert_exists
from commons.assertions import AssertionError
from commons.logger import log_section, log_success, log_error


def test_dump_flow():
    """Test flow: open app and navigate."""
    log_section("STARTING TEST FLOW")
    
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
    
    # Assertion: Kiểm tra kết quả cuối cùng
    from commons.logger import log_info
    log_info("Validating test result...")
    try:
        assert_exists(text_contains="Tiếp", timeout=5.0, message="Expected 'Tiếp' button not found")
        log_section("TEST PASSED", char="=")
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_dump_flow()

