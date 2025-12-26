"""Test case: Sử dụng assertions để validate test pass/fail."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, assert_exists, assert_not_exists
from commons.assertions import assert_text_in_dump, assert_text_not_in_dump


def test_assertions():
    """
    Test case: Sử dụng assertions để kiểm tra test pass/fail.
    
    Trường hợp sử dụng:
    - Kiểm tra element có tồn tại sau khi thực hiện action
    - Validate kết quả cuối cùng của test
    - Assert text có trong dump
    - Assert element không tồn tại (đã bị xóa/ẩn)
    """
    print("=" * 60)
    print("TEST: Assertions")
    print("=" * 60)
    
    setup_app()
    
    # Navigate và thực hiện actions
    steps = [
        touch("Khám phá"),
        touch("Hậu mãi VinFast"),
        touch("Đặt lịch dịch vụ"),
        touch("Đặt lịch dịch vụ", 1),
        touch("Bảo dưỡng"),
    ]
    execute_steps(steps)
    
    # Assertion: Kiểm tra text có trong dump (bước cuối để validate)
    print("\n[ASSERT] Validating test result...")
    
    # Cách 1: Dùng helper function trong steps
    steps_with_assert = [
        touch("Tiếp theo"),
        assert_exists(text_contains="Tỉnh/Thành phố"),  # Assert element tồn tại
    ]
    execute_steps(steps_with_assert)
    
    # Cách 2: Dùng assertion function trực tiếp
    assert_text_in_dump("Tỉnh/Thành phố", message="Expected text 'Tỉnh/Thành phố' not found")
    
    # Cách 3: Assert element không tồn tại
    assert_text_not_in_dump("Error", message="Unexpected error text found")
    
    # Cách 4: Assert với dict format
    steps_final = [
        {"assert": "exists", "text_contains": "Đà Nẵng", "timeout": 5.0},
        {"assert": "not_exists", "text_contains": "Lỗi", "timeout": 2.0},
    ]
    execute_steps(steps_final)
    
    print("\n" + "=" * 60)
    print("✓ TEST PASSED - All assertions passed")
    print("=" * 60)


def test_assertion_failure():
    """
    Test case: Demo assertion failure.
    
    Ví dụ khi assertion fail sẽ throw AssertionError.
    """
    print("=" * 60)
    print("TEST: Assertion Failure Demo")
    print("=" * 60)
    
    setup_app()
    
    try:
        # Assert element không tồn tại (sẽ fail)
        assert_text_in_dump("NonExistentText12345", timeout=2.0)
        print("\n[ASSERT] ✗ TEST FAILED - Should have raised AssertionError")
    except AssertionError as e:
        print(f"\n[ASSERT] ✓ Expected assertion failure: {e}")
        print("✓ TEST PASSED - Assertion correctly failed")


if __name__ == "__main__":
    test_assertions()
    # Uncomment to test failure case:
    # test_assertion_failure()

