"""Test case: Error handling và recovery."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, key
from core.waiter import Wait
from core.exceptions import TimeoutException
from config import settings


def test_error_handling():
    """
    Test case: Xử lý lỗi và recovery.
    
    Trường hợp sử dụng:
    - Element không tìm thấy
    - App crash/restart
    - Network error
    - Retry với logic khác
    """
    print("=" * 60)
    print("TEST: Error Handling and Recovery")
    print("=" * 60)
    
    setup_app()
    
    # Case 1: Try-catch với fallback
    try:
        print("\n[ERROR] Attempting to find element...")
        element = Wait(timeout=5).until_element(text_contains="Khám phá")
        element.click()
    except TimeoutException:
        print("[ERROR] Element not found, trying alternative...")
        # Fallback: thử text khác
        element = Wait(timeout=5).until_element(text_contains="Khám")
        element.click()
    
    # Case 2: Retry với logic khác
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"\n[ERROR] Attempt {attempt+1}/{max_retries}")
            element = Wait(timeout=3).until_element(text_contains="Button")
            element.click()
            break
        except TimeoutException:
            if attempt < max_retries - 1:
                print("[ERROR] Retrying...")
                # Có thể scroll hoặc làm gì đó trước khi retry
                key(4)  # Back
            else:
                print("[ERROR] Max retries reached, giving up")
                raise
    
    # Case 3: Error handling với dump tự động
    # DUMP_ON_ERROR=True trong config sẽ tự động dump khi có lỗi
    try:
        element = Wait(timeout=5).until_element(text_contains="NonExistent")
        element.click()
    except TimeoutException as e:
        print(f"[ERROR] Error occurred: {e}")
        print("[ERROR] Dump đã được tạo tự động (nếu DUMP_ON_ERROR=True)")
        # Có thể xử lý tiếp hoặc skip step này
    
    # Case 4: Continue execution sau error
    steps = [
        touch("Khám phá"),  # Step này sẽ chạy bình thường
        # Step có thể fail nhưng không dừng toàn bộ test
    ]
    
    for step in steps:
        try:
            execute_steps([step])
        except Exception as e:
            print(f"[ERROR] Step failed but continuing: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_error_handling()

