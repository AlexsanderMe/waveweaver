"""
Audio file selection component.
"""

import os
from pathlib import Path
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSizePolicy
from PySide6.QtCore import Qt, Signal

from ...config.settings import Settings
from ...utils.helpers import truncate_middle


class AudioSection(QFrame):
    """Component for audio file selection."""
    
    file_selected = Signal(str)
    
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.selected_file = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("Audio File")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #7aa2f7;")
        
        # File info label
        self.file_label = QLabel("No file selected")
        self.file_label.setWordWrap(True)
        
        # Select button
        self.select_btn = QPushButton("Select Audio File")
        self.select_btn.clicked.connect(self.select_file)
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.file_label)
        layout.addWidget(self.select_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def select_file(self):
        """Open file dialog to select audio file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.flac *.m4a *.ogg)"
        )
        
        if file_name:
            self.set_selected_file(file_name)
            self.file_selected.emit(file_name)
    
    def set_selected_file(self, file_path: str):
        """Set the selected file and update display."""
        self.selected_file = file_path
        display_name = truncate_middle(
            os.path.basename(file_path), 
            self.settings.ui.max_filename_display
        )
        self.file_label.setText(f"Selected: {display_name}")
    
    def get_selected_file(self) -> str:
        """Get the currently selected file."""
        return self.selected_file
    
    def clear_selection(self):
        """Clear the current file selection."""
        self.selected_file = None
        self.file_label.setText("No file selected")