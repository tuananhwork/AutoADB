"""Main entry point."""
import sys

# Import test_runner to use its functionality
from test_runner import run_all_tests, list_tests, discover_tests

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If arguments provided, use test_runner
        from test_runner import main
        main()
    else:
        # Default: run all tests
        print("Running all tests...")
        print("Use 'python test_runner.py -h' for more options")
        print("=" * 60)
        success = run_all_tests()
        sys.exit(0 if success else 1)

