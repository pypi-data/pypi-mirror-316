"""JAR file building functionality"""

import os
from typing import Dict, Any
from .file import FileManager, get_temp_dir, get_output_path, cleanup_temp_files
from .java import compile_java, create_jar
from .java_generator import generate_main_class
from .plugin_yml import generate_plugin_yml

class JarBuilder:
    """Handles building of the plugin JAR file"""
    
    def __init__(self, plugin_config: Dict[str, Any], output_dir: str):
        self.config = plugin_config
        self.output_dir = output_dir
        self.temp_dir = get_temp_dir()
        self.file_manager = FileManager()
        
    def build(self) -> str:
        """
        Build the plugin JAR file
        
        Returns:
            str: Path to the built JAR file
        """
        try:
            # Create temporary build structure
            src_dir = os.path.join(self.temp_dir, "src")
            resources_dir = os.path.join(self.temp_dir, "resources")
            classes_dir = os.path.join(self.temp_dir, "classes")
            
            self.file_manager.create_directory_structure([
                src_dir,
                resources_dir,
                classes_dir
            ])
            
            # Generate Java source files
            self._generate_sources(src_dir)
            
            # Generate plugin.yml
            plugin_yml = generate_plugin_yml(self.config)
            self.file_manager.write_file(
                os.path.join(resources_dir, "plugin.yml"),
                plugin_yml
            )
            
            # Compile Java sources
            compile_java(src_dir, classes_dir)
            
            # Create JAR file
            jar_path = get_output_path(
                self.output_dir,
                self.config['name'],
                self.config['version']
            )
            
            # Copy resources to classes directory
            self.file_manager.copy_resources(
                resources_dir,
                classes_dir
            )
            
            # Create JAR
            create_jar(jar_path, classes_dir)
            
            return jar_path
            
        finally:
            # Cleanup temporary directory
            cleanup_temp_files(self.temp_dir)
            
    def _generate_sources(self, src_dir: str) -> None:
        """Generate Java source files"""
        main_class = generate_main_class(self.config)
        package_path = os.path.join(
            src_dir, 
            self.config['name'].lower()
        )
        os.makedirs(package_path, exist_ok=True)
        
        self.file_manager.write_file(
            os.path.join(
                package_path,
                f"{self.config['name']}Plugin.java"
            ),
            main_class
        )