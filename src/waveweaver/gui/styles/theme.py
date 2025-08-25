"""
UI themes and styling definitions.
"""

from typing import Dict


class Theme:
    """Base theme class."""
    
    @property
    def stylesheet(self) -> str:
        """Get the complete stylesheet."""
        raise NotImplementedError


class DarkTheme(Theme):
    """Dark theme implementation."""
    
    # Color palette
    COLORS = {
        'background': '#1a1b26',
        'surface': '#24283b',
        'primary': '#7aa2f7',
        'primary_hover': '#89b4fa',
        'primary_pressed': '#6c91e1',
        'text': '#c0caf5',
        'text_muted': '#565f89',
        'border': '#414868',
        'disabled': '#414868',
        'disabled_text': '#565f89',
    }
    
    @property
    def stylesheet(self) -> str:
        """Get dark theme stylesheet."""
        return f"""
            QMainWindow {{
                background-color: {self.COLORS['background']};
            }}
            
            QFrame {{
                background-color: {self.COLORS['surface']};
                border-radius: 8px;
                border: 1px solid {self.COLORS['border']};
            }}
            
            QLabel {{
                color: {self.COLORS['text']};
                font-size: 14px;
                padding: 5px;
            }}
            
            QCheckBox {{
                color: {self.COLORS['text']};
                font-size: 14px;
                spacing: 8px;
                padding: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid {self.COLORS['border']};
            }}

            QCheckBox::indicator:checked {{
                background-color: {self.COLORS['primary']};
                border: 2px solid {self.COLORS['primary']};
            }}

            QCheckBox::indicator:pressed {{
                background-color: {self.COLORS['primary_pressed']};
                border: 2px solid {self.COLORS['primary_pressed']};
            }}
            
            QPushButton {{
                background-color: {self.COLORS['primary']};
                color: {self.COLORS['background']};
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }}
            
            QPushButton:hover {{
                background-color: {self.COLORS['primary_hover']};
            }}
            
            QPushButton:pressed {{
                background-color: {self.COLORS['primary_pressed']};
            }}
            
            QPushButton:disabled {{
                background-color: {self.COLORS['disabled']};
                color: {self.COLORS['disabled_text']};
            }}
            
            QProgressBar {{
                border: 2px solid {self.COLORS['border']};
                border-radius: 6px;
                text-align: center;
                color: {self.COLORS['text']};
                background-color: {self.COLORS['background']};
                height: 25px;
            }}
            
            QProgressBar::chunk {{
                background-color: {self.COLORS['primary']};
                border-radius: 4px;
            }}
            
            QComboBox {{
                background-color: {self.COLORS['background']};
                color: {self.COLORS['text']};
                border: 2px solid {self.COLORS['border']};
                border-radius: 6px;
                padding: 8px;
                min-width: 200px;
            }}
            
            QComboBox:hover {{
                border-color: {self.COLORS['primary']};
            }}
            
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {self.COLORS['background']};
                color: {self.COLORS['text']};
                selection-background-color: {self.COLORS['border']};
                border: 2px solid {self.COLORS['border']};
                border-radius: 6px;
            }}
        """


class LightTheme(Theme):
    """Light theme implementation."""
    
    # Color palette
    COLORS = {
        'background': '#f7f7f9',
        'surface': '#ffffff',
        'primary': '#4f6ef7',
        'primary_hover': '#3b5af0',
        'primary_pressed': '#2a4ae8',
        'text': '#2a2d3a',
        'text_muted': '#6c7293',
        'border': '#e1e5e9',
        'disabled': '#f1f3f4',
        'disabled_text': '#9aa0ac',
    }
    
    @property
    def stylesheet(self) -> str:
        """Get light theme stylesheet."""
        return f"""
            QMainWindow {{
                background-color: {self.COLORS['background']};
            }}
            
            QFrame {{
                background-color: {self.COLORS['surface']};
                border-radius: 8px;
                border: 1px solid {self.COLORS['border']};
            }}
            
            QLabel {{
                color: {self.COLORS['text']};
                font-size: 14px;
                padding: 5px;
            }}
            
            QCheckBox {{
                color: {self.COLORS['text']};
                font-size: 14px;
                spacing: 8px;
                padding: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid {self.COLORS['border']};
                background-color: {self.COLORS['surface']};
            }}

            QCheckBox::indicator:checked {{
                background-color: {self.COLORS['primary']};
                border: 2px solid {self.COLORS['primary']};
            }}

            QCheckBox::indicator:pressed {{
                background-color: {self.COLORS['primary_pressed']};
                border: 2px solid {self.COLORS['primary_pressed']};
            }}
            
            QPushButton {{
                background-color: {self.COLORS['primary']};
                color: {self.COLORS['surface']};
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }}
            
            QPushButton:hover {{
                background-color: {self.COLORS['primary_hover']};
            }}
            
            QPushButton:pressed {{
                background-color: {self.COLORS['primary_pressed']};
            }}
            
            QPushButton:disabled {{
                background-color: {self.COLORS['disabled']};
                color: {self.COLORS['disabled_text']};
            }}
            
            QProgressBar {{
                border: 2px solid {self.COLORS['border']};
                border-radius: 6px;
                text-align: center;
                color: {self.COLORS['text']};
                background-color: {self.COLORS['background']};
                height: 25px;
            }}
            
            QProgressBar::chunk {{
                background-color: {self.COLORS['primary']};
                border-radius: 4px;
            }}
            
            QComboBox {{
                background-color: {self.COLORS['surface']};
                color: {self.COLORS['text']};
                border: 2px solid {self.COLORS['border']};
                border-radius: 6px;
                padding: 8px;
                min-width: 200px;
            }}
            
            QComboBox:hover {{
                border-color: {self.COLORS['primary']};
            }}
            
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {self.COLORS['surface']};
                color: {self.COLORS['text']};
                selection-background-color: {self.COLORS['border']};
                border: 2px solid {self.COLORS['border']};
                border-radius: 6px;
            }}
        """
        

class ThemeManager:
    """Theme management class."""
    
    THEMES: Dict[str, Theme] = {
        'dark': DarkTheme(),
        'light': LightTheme(),
    }
    
    @classmethod
    def get_theme(cls, theme_name: str) -> Theme:
        """Get theme by name."""
        return cls.THEMES.get(theme_name, cls.THEMES['dark'])
    
    @classmethod
    def get_available_themes(cls) -> list:
        """Get list of available theme names."""
        return list(cls.THEMES.keys())