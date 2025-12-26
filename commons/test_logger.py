"""Test logger to capture and save test output to file."""
import sys
import os
import re
from datetime import datetime
from pathlib import Path
from typing import TextIO


class TestLogger:
    """Capture stdout/stderr and write to both console and file."""
    
    # ANSI escape sequence regex
    ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    def __init__(self, test_name: str, log_dir: str = "logs"):
        """
        Initialize test logger.
        
        Args:
            test_name: Name of the test (used for log filename)
            log_dir: Directory to save log files
        """
        self.test_name = test_name
        self.log_dir = Path(log_dir)
        self.log_file = None
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.log_path = None
        
        # Create log directory if not exists
        self.log_dir.mkdir(exist_ok=True)
        
        # Generate log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize test_name for filename
        safe_name = test_name.replace(".", "_").replace(" ", "_")
        log_filename = f"{safe_name}_{timestamp}.log"
        self.log_path = self.log_dir / log_filename
    
    @staticmethod
    def strip_ansi(text: str) -> str:
        """Remove ANSI escape sequences from text."""
        return TestLogger.ANSI_ESCAPE.sub('', text)
    
    def __enter__(self):
        """Start logging."""
        # Open log file
        self.log_file = open(self.log_path, 'w', encoding='utf-8')
        
        # Create Tee class to write to both console and file
        class Tee:
            def __init__(self, console_file, log_file, strip_ansi_func):
                self.console_file = console_file
                self.log_file = log_file
                self.strip_ansi = strip_ansi_func
            
            def write(self, data):
                # Write to console with colors
                self.console_file.write(data)
                self.console_file.flush()
                
                # Write to log file without colors
                clean_data = self.strip_ansi(data)
                self.log_file.write(clean_data)
                self.log_file.flush()
            
            def flush(self):
                self.console_file.flush()
                self.log_file.flush()
        
        # Redirect stdout and stderr
        sys.stdout = Tee(self.original_stdout, self.log_file, self.strip_ansi)
        sys.stderr = Tee(self.original_stderr, self.log_file, self.strip_ansi)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop logging and close file."""
        # Restore original stdout/stderr
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        
        # Close log file
        if self.log_file:
            self.log_file.close()
        
        return False
    
    def get_log_path(self):
        """Get the path to the log file."""
        return str(self.log_path)

