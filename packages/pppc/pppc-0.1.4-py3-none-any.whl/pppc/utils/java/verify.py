"""Java installation verification utilities"""

import subprocess

def verify_java_installation() -> bool:
    """
    Verify that Java is installed and available
    
    Returns:
        bool: True if Java is available, False otherwise
    """
    try:
        result = subprocess.run(
            ['java', '-version'], 
            capture_output=True, 
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False