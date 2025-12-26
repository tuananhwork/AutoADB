"""Test case: Debug với dump và screenshot."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch
from core import dump
from config import settings


def test_dump_debug():
    """
    Test case: Sử dụng dump và screenshot để debug.
    
    Trường hợp sử dụng:
    - Debug khi test fail
    - Kiểm tra UI state
    - Tạo evidence/report
    - Phân tích vấn đề
    """
    print("=" * 60)
    print("TEST: Dump and Screenshot for Debugging")
    print("=" * 60)
    
    setup_app()
    
    # Dump trước khi bắt đầu
    print("\n[DUMP] Initial dump...")
    xml_path, screenshot_path = dump.dump_ui("initial")
    print(f"[DUMP] XML: {xml_path}")
    print(f"[DUMP] Screenshot: {screenshot_path}")
    
    # Chạy một số steps
    steps = [
        "Khám phá",
        "Hậu mãi VinFast",
    ]
    execute_steps(steps)
    
    # Dump sau khi navigate
    print("\n[DUMP] After navigation...")
    xml_path, screenshot_path = dump.dump_ui("after_nav")
    print(f"[DUMP] XML: {xml_path}")
    print(f"[DUMP] Screenshot: {screenshot_path}")
    
    # Bật DUMP_ON_EACH_STEP để dump tự động
    print("\n[DUMP] Enabling DUMP_ON_EACH_STEP...")
    original_setting = settings.DUMP_ON_EACH_STEP
    settings.DUMP_ON_EACH_STEP = True
    
    try:
        steps_with_dump = [
            "Đặt lịch dịch vụ",
            ("Đặt lịch dịch vụ", 1),
            "Bảo dưỡng",
        ]
        execute_steps(steps_with_dump)
    finally:
        # Restore setting
        settings.DUMP_ON_EACH_STEP = original_setting
    
    # Dump cuối cùng
    print("\n[DUMP] Final dump...")
    xml_path, screenshot_path = dump.dump_ui("final")
    print(f"[DUMP] XML: {xml_path}")
    print(f"[DUMP] Screenshot: {screenshot_path}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)
    print("\n[DUMP] All dumps saved in artifacts/ directory")


if __name__ == "__main__":
    test_dump_debug()

