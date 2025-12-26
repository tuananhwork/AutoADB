"""Test case: Tap và swipe theo tọa độ."""
from commons.setup import setup_app
from commons.helpers import execute_steps, tap, swipe


def test_coordinates():
    """
    Test case: Sử dụng tap và swipe theo tọa độ.
    
    Trường hợp sử dụng:
    - Element không có text hoặc text không ổn định
    - Cần tap tại vị trí cố định
    - Cần swipe để scroll/navigate
    - Element là image/icon không có text
    """
    print("=" * 60)
    print("TEST: Tap and Swipe by Coordinates")
    print("=" * 60)
    
    setup_app()
    
    steps = [
        # Touch by text
        "Khám phá",
        
        # Tap tại tọa độ cụ thể (ví dụ: center screen)
        tap(540, 1200),
        
        # Swipe lên để scroll
        swipe(540, 1500, 540, 500, duration=500),
        
        # Swipe xuống
        swipe(540, 500, 540, 1500, duration=500),
        
        # Swipe sang trái
        swipe(900, 1200, 100, 1200, duration=300),
        
        # Swipe sang phải
        swipe(100, 1200, 900, 1200, duration=300),
        
        # Tap tại vị trí khác
        tap(200, 800),
    ]
    
    execute_steps(steps)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_coordinates()

