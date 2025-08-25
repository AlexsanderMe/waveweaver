"""
Application configuration and settings management.
"""

import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class WindowSettings:
    """Window-related settings."""
    width: int = 930
    height: int = 650
    min_width: int = 800
    min_height: int = 600


@dataclass
class ModelSettings:
    """Model-related settings."""
    default_model: str = "htdemucs_ft"
    cache_dir: str = "./models"
    shifts: int = 2


@dataclass
class UISettings:
    """UI-related settings."""
    theme: str = "dark"
    max_filename_display: int = 40
    progress_update_interval: int = 100


class Settings:
    """Main settings class."""
    
    def __init__(self):
        self.window = WindowSettings()
        self.model = ModelSettings()
        self.ui = UISettings()
        self._load_from_environment()
    
    def _load_from_environment(self):
        """Load settings from environment variables."""
        # Window settings
        self.window.width = int(os.getenv("WAVEWEAVER_WINDOW_WIDTH", self.window.width))
        self.window.height = int(os.getenv("WAVEWEAVER_WINDOW_HEIGHT", self.window.height))
        
        # Model settings
        self.model.default_model = os.getenv("DEFAULT_MODEL", self.model.default_model)
        self.model.cache_dir = os.getenv("DEMUCS_CACHE_DIR", self.model.cache_dir)
        self.model.shifts = int(os.getenv("DEMUCS_SHIFTS", self.model.shifts))
        
        # UI settings
        self.ui.theme = os.getenv("THEME", self.ui.theme)
    
    def get_assets_path(self) -> Path:
        """Get path to assets directory."""
        return Path(__file__).parent.parent.parent.parent / "assets"
    
    def get_icon_path(self, icon_name: str) -> Path:
        """Get path to specific icon."""
        return self.get_assets_path() / "icons" / icon_name