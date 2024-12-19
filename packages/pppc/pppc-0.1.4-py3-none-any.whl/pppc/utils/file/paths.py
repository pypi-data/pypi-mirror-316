"""Path management utilities"""

import os
import tempfile
from typing import Optional

def get_temp_dir() -> str:
    """
    Create and return a temporary directory
    
    Returns:
        str: Path to temporary directory
    """
    return tempfile.mkdtemp(prefix='pppc_')

def get_output_path(
    output_dir: str,
    name: str,
    version: str,
    create_dirs: bool = True
) -> str:
    """
    Get the output path for a file
    
    Args:
        output_dir: Base output directory
        name: Plugin name
        version: Plugin version
        create_dirs: Whether to create directories
        
    Returns:
        str: Full output path
    """
    if create_dirs:
        os.makedirs(output_dir, exist_ok=True)
        
    return os.path.join(
        output_dir,
        f"{name.lower()}-{version}.jar"
    )