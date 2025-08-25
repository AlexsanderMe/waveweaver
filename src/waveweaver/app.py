"""
Application bootstrap and main entry point.
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from .gui.main_window import MainWindow
from .config.settings import Settings


def setup_application():
    """Configure QApplication with proper settings."""
    app = QApplication(sys.argv)
    
    # Enable high DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Set application metadata
    app.setApplicationName("WaveWeaver")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AlexsanderMe")
    app.setOrganizationDomain("github.com/AlexsanderMe")
    
    # Set application icon
    icon_path = Path(__file__).parent.parent.parent / "assets" / "icons" / "ico.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    return app


def main():
    """Main application entry point."""
    try:
        # Initialize settings
        settings = Settings()
        
        # Setup QApplication
        app = setup_application()
        
        # Create and show main window
        window = MainWindow(settings)
        window.show()
        
        # Start event loop
        return app.exec()
    
    except Exception as e:
        print(f"Failed to start WaveWeaver: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())