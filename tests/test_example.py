"""Example test using common setup."""
from commons.setup import setup_app, teardown_app
from commons.helpers import execute_steps


def test_example_flow():
    """Example test flow using common setup."""
    print("=" * 60)
    print("STARTING EXAMPLE TEST")
    print("=" * 60)
    
    try:
        # Common setup
        setup_app()
        
        # Test-specific steps
        steps = [
            ("[STEP 1] Touch 'Some button'", "Some button"),
            ("[STEP 2] Touch 'Another button'", "Another button"),
        ]
        
        execute_steps(steps, start_step_num=1)
        
    finally:
        # Common teardown (optional)
        # teardown_app()
        pass
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_example_flow()

