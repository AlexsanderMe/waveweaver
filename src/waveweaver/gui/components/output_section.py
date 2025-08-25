"""
Output folder selection component.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSizePolicy
from PySide6.QtCore import Qt, Signal

from ...config.settings import Settings


class OutputSection(QFrame):
    """Component for output folder selection."""
    
    folder_selected = Signal(str)
    
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.selected_folder = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("Output Folder")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #7aa2f7;")
        
        # Folder info label
        self.folder_label = QLabel("No folder selected")
        self.folder_label.setWordWrap(True)
        
        # Select button
        self.select_btn = QPushButton("Select Output Folder")
        self.select_btn.clicked.connect(self.select_folder)
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.select_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def select_folder(self):
        """Open folder dialog to select output directory."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory"
        )
        
        if folder:
            self.set_selected_folder(folder)
            self.folder_selected.emit(folder)
    
    def set_selected_folder(self, folder_path: str):
        """Set the selected folder and update display."""
        self.selected_folder = folder_path
        
        # Show truncated path if too long
        display_path = folder_path
        max_display = self.settings.ui.max_filename_display
        if len(folder_path) > max_display:
            display_path = "..." + folder_path[-max_display:]
        
        self.folder_label.setText(f"Selected: {display_path}")
    
    def get_selected_folder(self) -> str:
        """Get the currently selected folder."""
        return self.selected_folder
    
    def clear_selection(self):
        """Clear the current folder selection."""
        self.selected_folder = None
        self.folder_label.setText("No folder selected")