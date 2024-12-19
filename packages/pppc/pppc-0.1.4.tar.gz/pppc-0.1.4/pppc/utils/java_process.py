"""Java process execution utilities"""

import os
import subprocess
from typing import List, Optional
from ..exceptions import CompilationError

class JavaProcessManager:
    """Manages Java process execution for compilation and JAR creation"""
    
    @staticmethod
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
            
    @staticmethod
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
            
    @staticmethod
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