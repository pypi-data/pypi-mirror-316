"""Java compilation utilities"""

import os
import subprocess
from typing import List, Optional
from ...exceptions import CompilationError

def compile_java(
    src_dir: str, 
    output_dir: str, 
    classpath: Optional[List[str]] = None
) -> None:
    """
    Compile Java source files using javac
    
    Args:
        src_dir: Source directory containing .java files
        output_dir: Output directory for .class files
        classpath: Optional list of classpath entries
        
    Raises:
        CompilationError: If compilation fails
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = ['javac']
        if classpath:
            cmd.extend(['-cp', os.pathsep.join(classpath)])
            
        cmd.extend([
            '-d', output_dir,
            *[os.path.join(root, f) 
              for root, _, files in os.walk(src_dir)
              for f in files if f.endswith('.java')]
        ])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise CompilationError(
                f"Java compilation failed: {result.stderr}"
            )
            
    except Exception as e:
        raise CompilationError(f"Compilation error: {str(e)}")