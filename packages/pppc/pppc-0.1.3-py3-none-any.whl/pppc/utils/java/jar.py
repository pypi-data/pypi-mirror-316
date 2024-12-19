"""JAR file creation utilities"""

import subprocess
from typing import Optional
from ...exceptions import CompilationError

def create_jar(
    jar_path: str,
    class_dir: str,
    manifest_path: Optional[str] = None
) -> None:
    """
    Create JAR file from compiled classes
    
    Args:
        jar_path: Output JAR file path
        class_dir: Directory containing compiled classes
        manifest_path: Optional path to MANIFEST.MF
        
    Raises:
        CompilationError: If JAR creation fails
    """
    try:
        cmd = ['jar', 'cf', jar_path]
        
        if manifest_path:
            cmd.extend(['-m', manifest_path])
            
        cmd.extend(['-C', class_dir, '.'])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise CompilationError(
                f"JAR creation failed: {result.stderr}"
            )
            
    except Exception as e:
        raise CompilationError(f"JAR creation error: {str(e)}")