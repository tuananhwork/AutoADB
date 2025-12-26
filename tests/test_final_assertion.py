"""Test case: Assertion ở bước cuối để validate test pass/fail."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_success, log_error, log_info


def test_with_final_assertion():
    """
    Test case: Sử dụng assertion ở bước cuối để validate test.
    
    Pattern:
    1. Chạy các steps
    2. Ở bước cuối, assert text có trong dump
    3. Nếu assert pass → test pass (màu xanh)
    4. Nếu assert fail → test fail (màu đỏ, throw AssertionError)
    """
    log_section("TEST: Final Assertion Pattern")
    
    try:
        setup_app()
        
        # Chạy các steps
        steps = [
            "Khám phá",
            "Hậu mãi VinFast",
            "Đặt lịch dịch vụ",
            ("Đặt lịch dịch vụ", 1),
            "Bảo dưỡng",
            "Tiếp theo",
            "Tỉnh/Thành phố",
            "Đà Nẵng",
            "Chọn tỉnh",
        ]
        execute_steps(steps)
        
        # Bước cuối: Assert để validate test pass/fail
        log_info("Final validation...")
        assert_text_in_dump("Chọn xưởng dịch vụ", timeout=5.0, 
                           message="Test FAILED: Expected 'Chọn xưởng dịch vụ' not found")
        
        # Nếu đến đây → test PASSED (màu xanh)
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        # Assertion fail → test FAILED (màu đỏ)
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        # Lỗi khác → test FAILED (màu đỏ)
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_with_final_assertion()

