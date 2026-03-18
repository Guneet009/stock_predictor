import os
from pathlib import Path
import sys
import yaml

class ConfigLoader:
    """
    Central configuration loader for the project.

    Loads YAML configuration files and provides convenient access
    across the application.
    """

    def __init__(self,config_path:str="configs/config.yaml"):
        self.project_root = self._get_project_root()
        self.config_path = self.project_root/config_path
        self.config = self._load_config()
    
    def _get_project_root(self) -> Path:
        """
        Detect project root directory dynamically.
        """
        return Path(__file__).resolve().parents[3]
    
    def _load_config(self):
        """
        Load YAML configuration file.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Config file not found at {self.config_path}"
            )

        with open(self.config_path,"r") as file:
            return yaml.safe_load(file)
    
    def get(self,key:str, default=None):
        """
        Get configuration value by key.
        """
        return self.config.get(key,default)
    
    def get_section(self,section:str):
        """
        Retrieve a full configuration section.
        """
        return self.config.get(section,{})
    
    def get_path(self,path_key:str) -> Path:
        """
        Retrieve a full configuration section.
        """
        paths = self.config.get("data_paths",{})
        if path_key not in paths:
            raise KeyError(f"Path key '{path_key} not found in config'")
        
        return self.project_root/paths[path_key]

# Singleton instance across project
config = ConfigLoader()