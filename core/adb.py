"""ADB command wrapper."""
import subprocess
import sys
from config import device


def run(cmd: str) -> str:
    """
    Run ADB command and return output.
    
    Args:
        cmd: ADB command (without 'adb' prefix)
        
    Returns:
        Command output as string
        
    Raises:
        RuntimeError: If ADB command fails
    """
    full_cmd = ["adb"]
    
    # Add device ID if specified
    if device.DEVICE_ID:
        full_cmd.extend(["-s", device.DEVICE_ID])
    
    # Add custom options
    full_cmd.extend(device.ADB_OPTIONS)
    
    # Add the actual command
    full_cmd.extend(cmd.split())
    
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ADB command failed: {' '.join(full_cmd)}\nError: {e.stderr}")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"ADB command timeout: {' '.join(full_cmd)}")

