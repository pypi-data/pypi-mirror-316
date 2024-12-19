"""Cleanup utilities"""

import os
import shutil
from typing import Optional

def cleanup_temp_files(temp_dir: str, ignore_errors: bool = True) -> None:
    """
    Clean up temporary files and directories
    
    Args:
        temp_dir: Directory to clean up
        ignore_errors: Whether to ignore errors during cleanup
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=ignore_errors)