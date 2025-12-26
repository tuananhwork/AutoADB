"""Test runner to execute multiple test cases."""
import sys
import importlib
import argparse
from pathlib import Path
from commons.logger import log_section, log_success, log_error, log_info
from commons.test_logger import TestLogger


def discover_tests():
    """Discover all test functions in tests directory."""
    tests_dir = Path("tests")
    test_files = sorted(tests_dir.glob("test_*.py"))
    
    all_tests = {}
    for test_file in test_files:
        module_name = f"tests.{test_file.stem}"
        try:
            module = importlib.import_module(module_name)
            # Find all functions starting with 'test_'
            for name in dir(module):
                if name.startswith("test_") and callable(getattr(module, name)):
                    test_key = f"{test_file.stem}.{name}"
                    all_tests[test_key] = (module, name)
        except Exception as e:
            log_error(f"Failed to import {module_name}: {e}")
    
    return all_tests


def run_test(module, test_name, enable_logging=True):
    """
    Run a single test function.
    
    Args:
        module: Module containing the test
        test_name: Name of test function
        enable_logging: Whether to save log to file
        
    Returns:
        Tuple of (success: bool, log_path: str or None)
    """
    log_path = None
    
    if enable_logging:
        # Create full test identifier
        test_identifier = f"{module.__name__}.{test_name}"
        with TestLogger(test_identifier) as logger:
            try:
                test_func = getattr(module, test_name)
                log_section(f"Running: {test_name}")
                log_info(f"Log file: {logger.get_log_path()}")
                test_func()
                log_success(f"Test passed: {test_name}")
                log_path = logger.get_log_path()
                return True, log_path
            except AssertionError as e:
                log_error(f"Test failed (assertion): {test_name} - {e}")
                log_path = logger.get_log_path()
                return False, log_path
            except Exception as e:
                log_error(f"Test failed (error): {test_name} - {e}")
                log_path = logger.get_log_path()
                return False, log_path
    else:
        # Run without file logging
        try:
            test_func = getattr(module, test_name)
            log_section(f"Running: {test_name}")
            test_func()
            log_success(f"Test passed: {test_name}")
            return True, None
        except AssertionError as e:
            log_error(f"Test failed (assertion): {test_name} - {e}")
            return False, None
        except Exception as e:
            log_error(f"Test failed (error): {test_name} - {e}")
            return False, None


def run_all_tests(enable_logging=True):
    """Run all discovered tests."""
    all_tests = discover_tests()
    
    if not all_tests:
        log_error("No tests found!")
        return False
    
    log_section(f"Found {len(all_tests)} test(s)")
    
    results = {"passed": 0, "failed": 0, "total": len(all_tests)}
    log_files = []
    
    for test_key, (module, test_name) in all_tests.items():
        passed, log_path = run_test(module, test_name, enable_logging=enable_logging)
        if passed:
            results["passed"] += 1
        else:
            results["failed"] += 1
        if log_path:
            log_files.append((test_key, log_path, passed))
        print()  # Empty line between tests
    
    # Summary
    log_section("Test Summary")
    log_info(f"Total: {results['total']}")
    log_success(f"Passed: {results['passed']}")
    if results["failed"] > 0:
        log_error(f"Failed: {results['failed']}")
    else:
        log_success("All tests passed!")
    
    # Show log files
    if enable_logging and log_files:
        print()
        log_section("Log Files")
        for test_key, log_path, passed in log_files:
            status = "[PASS]" if passed else "[FAIL]"
            log_info(f"{status} {test_key}: {log_path}")
    
    return results["failed"] == 0


def run_tests_by_pattern(pattern, enable_logging=True):
    """Run tests matching a pattern."""
    all_tests = discover_tests()
    matching_tests = {
        k: v for k, v in all_tests.items()
        if pattern.lower() in k.lower()
    }
    
    if not matching_tests:
        log_error(f"No tests found matching pattern: {pattern}")
        return False
    
    log_section(f"Found {len(matching_tests)} test(s) matching '{pattern}'")
    
    results = {"passed": 0, "failed": 0}
    log_files = []
    
    for test_key, (module, test_name) in matching_tests.items():
        passed, log_path = run_test(module, test_name, enable_logging=enable_logging)
        if passed:
            results["passed"] += 1
        else:
            results["failed"] += 1
        if log_path:
            log_files.append((test_key, log_path, passed))
        print()
    
    log_section("Test Summary")
    log_info(f"Total: {len(matching_tests)}")
    log_success(f"Passed: {results['passed']}")
    if results["failed"] > 0:
        log_error(f"Failed: {results['failed']}")
    
    # Show log files
    if enable_logging and log_files:
        print()
        log_section("Log Files")
        for test_key, log_path, passed in log_files:
            status = "[PASS]" if passed else "[FAIL]"
            log_info(f"{status} {test_key}: {log_path}")
    
    return results["failed"] == 0


def list_tests():
    """List all available tests."""
    all_tests = discover_tests()
    
    if not all_tests:
        log_error("No tests found!")
        return
    
    log_section(f"Available Tests ({len(all_tests)})")
    for i, test_key in enumerate(sorted(all_tests.keys()), 1):
        log_info(f"{i}. {test_key}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test runner for ADB automation framework")
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Run all tests"
    )
    parser.add_argument(
        "-p", "--pattern",
        type=str,
        help="Run tests matching pattern (e.g., 'basic', 'assertion')"
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all available tests"
    )
    parser.add_argument(
        "-t", "--test",
        type=str,
        help="Run specific test (format: test_file.test_function, e.g., 'test_dump.test_dump_flow')"
    )
    parser.add_argument(
        "--no-log",
        action="store_true",
        help="Disable file logging (output to console only)"
    )
    
    args = parser.parse_args()
    enable_logging = not args.no_log
    
    if args.list:
        list_tests()
        return
    
    if args.all:
        success = run_all_tests(enable_logging=enable_logging)
        sys.exit(0 if success else 1)
    
    if args.pattern:
        success = run_tests_by_pattern(args.pattern, enable_logging=enable_logging)
        sys.exit(0 if success else 1)
    
    if args.test:
        # Parse test name: test_file.test_function
        parts = args.test.split(".")
        if len(parts) == 2:
            test_file, test_func = parts
            module_name = f"tests.{test_file}"
            try:
                module = importlib.import_module(module_name)
                success, log_path = run_test(module, test_func, enable_logging=enable_logging)
                if enable_logging and log_path:
                    print()
                    log_section("Log File")
                    log_info(f"Log saved to: {log_path}")
                sys.exit(0 if success else 1)
            except ImportError:
                log_error(f"Test file not found: {test_file}")
                sys.exit(1)
            except AttributeError:
                log_error(f"Test function not found: {test_func} in {test_file}")
                sys.exit(1)
        else:
            log_error("Invalid test format. Use: test_file.test_function")
            sys.exit(1)
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()

