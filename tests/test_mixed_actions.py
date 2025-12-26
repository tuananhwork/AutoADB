"""Example test with mixed actions."""
from commons.setup import setup_app
from commons.helpers import execute_steps, touch, tap, swipe, key, sleep


def test_mixed_actions():
    """Test flow with mixed action types."""
    print("=" * 60)
    print("STARTING MIXED ACTIONS TEST")
    print("=" * 60)
    
    # Common setup
    setup_app()
    
    # Mixed actions - can combine touch, tap, swipe, key, sleep
    steps = [
        # Touch by text (backward compatible - simple format)
        "Khám phá",
        ("Hậu mãi VinFast", 0),
        
        # Using helper functions (cleaner)
        touch("Đặt lịch dịch vụ", nth=0),
        touch("Bảo dưỡng"),
        tap(540, 1200),  # Tap at center
        swipe(540, 1500, 540, 500, duration=500),  # Swipe up
        sleep(2.0),  # Wait 2 seconds
        key(4),  # BACK button (code 4)
        touch("Tiếp theo"),
        
        # Or use dict format directly (more verbose but flexible)
        # {"action": "touch", "text": "Button", "nth": 1, "wait_after": 2.0},
    ]
    
    execute_steps(steps)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_mixed_actions()

