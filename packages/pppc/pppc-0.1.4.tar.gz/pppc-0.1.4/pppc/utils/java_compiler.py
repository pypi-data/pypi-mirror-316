"""Java compilation utilities"""

import os
import subprocess
from typing import List, Optional
from ..exceptions import CompilationError

class JavaCompiler:
    """Handles Java source compilation"""
    
    def __init__(self, src_dir: str, classpath: Optional[List[str]] = None):
        self.src_dir = src_dir
        self.classpath = classpath or []
        
    def compile(self, output_dir: str) -> None:
        """
        Compile Java source files
        
        Args:
            output_dir: Directory for compiled classes
            
        Raises:
            CompilationError: If compilation fails
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            cmd = ['javac']
            if self.classpath:
                cmd.extend(['-cp', os.pathsep.join(self.classpath)])
                
            cmd.extend([
                '-d', output_dir,
                *[os.path.join(root, f) 
                  for root, _, files in os.walk(self.src_dir)
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