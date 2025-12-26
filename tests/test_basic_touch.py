"""Test case: Basic touch by text - Trường hợp cơ bản nhất."""
from commons.setup import setup_app
from commons.helpers import execute_steps
from commons.assertions import assert_text_in_dump, AssertionError
from commons.logger import log_section, log_info


def test_basic_touch():
    """
    Test case cơ bản: Touch các element theo text.
    
    Trường hợp sử dụng:
    - Test flow đơn giản, chỉ cần touch theo text
    - Không cần xử lý đặc biệt
    - Format ngắn gọn nhất
    """
    log_section("TEST: Basic Touch by Text")
    
    try:
        setup_app()
        
        # Format đơn giản nhất - chỉ cần text
        steps = [
            "Khám phá",
            "Hậu mãi VinFast",
            "Đặt lịch dịch vụ",
            ("Đặt lịch dịch vụ", 1),
            "Bảo dưỡng",
            "Tiếp theo",
        ]
        
        execute_steps(steps)
        
        # Assertion: Validate test result
        log_info("Validating test result...")
        assert_text_in_dump("Tỉnh/Thành phố", timeout=5.0,
                           message="Test FAILED: Expected 'Tỉnh/Thành phố' not found")
        
        log_section("TEST PASSED", char="=")
        
    except AssertionError as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise
    except Exception as e:
        log_section(f"TEST FAILED: {e}", char="=")
        raise


if __name__ == "__main__":
    test_basic_touch()

