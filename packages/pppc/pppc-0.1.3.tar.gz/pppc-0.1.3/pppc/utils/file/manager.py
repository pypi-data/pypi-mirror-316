"""File management core functionality"""

import os
from typing import List

class FileManager:
    """Manages file operations during compilation"""
    
    @staticmethod
    def create_directory_structure(base_dir: str, directories: List[str]) -> None:
        """Create required directories"""
        for directory in directories:
            os.makedirs(os.path.join(base_dir, directory), exist_ok=True)
            
    @staticmethod
    def write_file(path: str, content: str) -> None:
        """Write content to file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    @staticmethod
    def copy_resources(src_dir: str, dest_dir: str) -> None:
        """Copy resource files"""
        if os.path.exists(src_dir):
            for root, _, files in os.walk(src_dir):
                rel_path = os.path.relpath(root, src_dir)
                dest_path = os.path.join(dest_dir, rel_path)
                os.makedirs(dest_path, exist_ok=True)
                
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_path, file)
                    with open(src_file, 'rb') as sf, open(dest_file, 'wb') as df:
                        df.write(sf.read())