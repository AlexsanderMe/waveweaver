"""
Main application window.
"""

import sys
import subprocess
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QFrame, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, QUrl, QMimeData
from PySide6.QtGui import QIcon, QDesktopServices

from ..config.settings import Settings
from ..core.models import ProcessingStatus, ProcessingResult, AvailableModels
from ..core.stem_separator import StemSeparatorThread
from ..utils.helpers import truncate_middle
from .styles.theme import ThemeManager
from .components.audio_section import AudioSection
from .components.model_selection import ModelSelection
from .components.stem_selection import StemSelection
from .components.output_section import OutputSection
from .components.progress_section import ProgressSection


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.separator_thread: Optional[StemSeparatorThread] = None
        self.artificial_progress_timer: Optional[QTimer] = None
        self.current_artificial_progress = 20
        
        # Window properties
        self.input_file: Optional[str] = None
        self.output_dir: Optional[str] = None
        
        self.setup_ui()
        self.connect_signals()

        self.initialize_default_model()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Window configuration
        self.setWindowTitle("WaveWeaver")
        self.setMinimumSize(
            self.settings.window.min_width, 
            self.settings.window.min_height
        )
        self.resize(self.settings.window.width, self.settings.window.height)
        
        # Set window icon
        icon_path = self.settings.get_icon_path("ico.ico")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
        # Apply theme
        theme = ThemeManager.get_theme(self.settings.ui.theme)
        self.setStyleSheet(theme.stylesheet)
        
        # Setup main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Main content container
        container = QFrame()
        container_layout = QHBoxLayout(container)
        container_layout.setSpacing(15)
        container_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create UI components
        self.audio_section = AudioSection(self.settings)
        self.model_selection = ModelSelection(self.settings)
        self.progress_section = ProgressSection(self.settings)
        self.stem_selection = StemSelection(self.settings)
        self.output_section = OutputSection(self.settings)
        
        # Left column
        left_column = self._create_left_column()
        left_widget = QWidget()
        left_widget.setFixedWidth(int(self.width() * 0.45))
        left_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        left_widget.setLayout(left_column)
        
        # Right column  
        right_column = self._create_right_column()
        right_widget = QWidget()
        right_widget.setFixedWidth(int(self.width() * 0.45))
        right_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        right_widget.setLayout(right_column)
        
        # Add columns to container
        container_layout.addWidget(left_widget)
        container_layout.addStretch()
        container_layout.addWidget(right_widget)
        
        main_layout.addWidget(container)
        
        # Add creator section
        self._add_creator_section(main_layout)
        
        # Store widgets for resize events
        self._left_widget = left_widget
        self._right_widget = right_widget
    

    def initialize_default_model(self):
        """Initialize the default model and update stems accordingly."""
        default_model = self.model_selection.get_selected_model()
        self.on_model_changed(default_model)
    
    def _create_left_column(self) -> QVBoxLayout:
        """Create the left column layout."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        layout.addWidget(self.audio_section)
        layout.addWidget(self.model_selection)
        layout.addWidget(self.progress_section)
        
        return layout
    
    def _create_right_column(self) -> QVBoxLayout:
        """Create the right column layout."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        layout.addWidget(self.stem_selection)
        layout.addWidget(self.output_section)
        layout.addWidget(self._create_button_section())
        layout.addStretch()
        
        return layout
    
    def _create_button_section(self) -> QFrame:
        """Create the button section."""
        from PySide6.QtWidgets import QPushButton
        
        button_frame = QFrame()
        button_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(15)
        
        self.extract_btn = QPushButton("Extract Stems")
        self.extract_btn.setEnabled(False)
        self.extract_btn.setFixedWidth(150)
        
        self.cancel_btn = QPushButton("Force Cancel")
        self.cancel_btn.setVisible(False)
        self.cancel_btn.setFixedWidth(150)
        
        button_layout.addStretch()
        button_layout.addWidget(self.extract_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        
        return button_frame
    
    def _add_creator_section(self, main_layout: QVBoxLayout):
        """Add creator section at the bottom."""
        from PySide6.QtWidgets import QPushButton
        
        creator_layout = QHBoxLayout()
        creator_layout.setContentsMargins(0, 0, 0, 0)
        creator_layout.setSpacing(10)
        
        coffee_btn = QPushButton("AlexsanderMe")
        coffee_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7aa2f7;
                border: none;
                padding: 5px 10px;
                font-size: 12px;
                min-width: 0px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #89b4fa;
                background-color: transparent;
            }
        """)
        
        github_icon_path = self.settings.get_icon_path("github.png")
        if github_icon_path.exists():
            coffee_btn.setIcon(QIcon(str(github_icon_path)))
        
        coffee_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        creator_layout.addStretch()
        creator_layout.addWidget(coffee_btn)
        creator_layout.addStretch()
        
        main_layout.addLayout(creator_layout)
        
        # Connect signal
        coffee_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/AlexsanderMe"))
        )
    
    def connect_signals(self):
        """Connect all UI signals."""
        # Audio section
        self.audio_section.file_selected.connect(self.on_file_selected)
        
        # Model selection
        self.model_selection.model_changed.connect(self.on_model_changed)
        
        # Output section  
        self.output_section.folder_selected.connect(self.on_output_folder_selected)
        
        # Buttons
        self.extract_btn.clicked.connect(self.start_extraction)
        self.cancel_btn.clicked.connect(self.force_cancel)
    
    def on_file_selected(self, file_path: str):
        """Handle file selection."""
        self.input_file = file_path
        self.update_extract_button_state()
    
    def on_model_changed(self, model_key: str):
        """Handle model selection change."""
        model_info = AvailableModels.get_model(model_key)
        self.stem_selection.update_stems(model_info.stems)
    
    def on_output_folder_selected(self, folder_path: str):
        """Handle output folder selection."""
        self.output_dir = folder_path
        self.update_extract_button_state()
    
    def update_extract_button_state(self):
        """Update the extract button enabled state."""
        can_extract = bool(
            self.input_file and 
            self.output_dir and 
            self.separator_thread is None
        )
        self.extract_btn.setEnabled(can_extract)
    
    def start_extraction(self):
        """Start the stem extraction process."""
        if not self.input_file or not self.output_dir:
            return
        
        selected_stems = self.stem_selection.get_selected_stems()
        if not selected_stems:
            QMessageBox.warning(self, "Warning", "Please select at least one stem")
            return
        
        # Setup UI for processing
        self.progress_section.start_processing()
        self.extract_btn.setEnabled(False)
        self.cancel_btn.setVisible(True)
        
        # Create and start processing thread
        model_key = self.model_selection.get_selected_model()
        self.separator_thread = StemSeparatorThread(
            self.input_file,
            self.output_dir,
            selected_stems,
            model_key
        )
        
        # Connect thread signals
        self.separator_thread.progress.connect(self.progress_section.update_progress)
        self.separator_thread.status_changed.connect(self.progress_section.update_status)
        self.separator_thread.error.connect(self.handle_error)
        self.separator_thread.finished.connect(self.on_extraction_complete)
        self.separator_thread.device_info.connect(self.progress_section.update_device_info)
        self.separator_thread.audio_info.connect(self.progress_section.update_audio_info)
        self.separator_thread.artificial_progress_finished.connect(
            self.progress_section.stop_artificial_progress
        )
        
        self.separator_thread.start()
        
        # Start artificial progress after delay
        QTimer.singleShot(1500, self.progress_section.start_artificial_progress)
    
    def force_cancel(self):
        """Force cancel the current operation."""
        if self.separator_thread:
            reply = QMessageBox.warning(
                self,
                "Warning",
                "The application will restart after canceling.\nDo you want to proceed?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self._restart_application()
    
    def handle_error(self, error_msg: str):
        """Handle processing errors."""
        QMessageBox.critical(self, "Error", f"An error occurred: {error_msg}")
        self.on_extraction_complete(ProcessingResult(False, [], error_msg))
    
    def on_extraction_complete(self, result: ProcessingResult):
        """Handle extraction completion."""
        self.progress_section.stop_processing()
        self.extract_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)
        
        if result.success:
            self.progress_section.show_completion_message(
                f"Extraction complete! ({result.processing_time:.1f}s)"
            )
        else:
            self.progress_section.show_error_message("Extraction failed!")
        
        if self.separator_thread:
            self.separator_thread.wait()
            self.separator_thread = None
    
    def _restart_application(self):
        """Restart the application."""
        if getattr(sys, 'frozen', False):
            app_path = sys.executable
        else:
            app_path = sys.argv[0]
        
        restart_script = """
import os
import sys
import time
import subprocess

time.sleep(0.5)
if sys.argv[1].endswith('.exe'):
    os.startfile(sys.argv[1])
else:
    subprocess.Popen([sys.executable, sys.argv[1]])
os.remove(sys.argv[0])
        """
        
        temp_script = Path(app_path).parent / "_restart.py"
        with open(temp_script, "w") as f:
            f.write(restart_script)
        
        subprocess.Popen([sys.executable, str(temp_script), app_path], 
                        creationflags=subprocess.CREATE_NO_WINDOW)
        
        from PySide6.QtWidgets import QApplication
        QApplication.quit()
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.separator_thread:
            reply = QMessageBox.warning(
                self,
                "Warning",
                "A process is still running.\nDo you want to force close?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    
    def resizeEvent(self, event):
        """Handle window resize."""
        width = event.size().width()
        column_width = int(width * 0.45)
        self._left_widget.setFixedWidth(column_width)
        self._right_widget.setFixedWidth(column_width)
        super().resizeEvent(event)
    
    # Drag and drop support
    def dragEnterEvent(self, event):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if file_path.lower().endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg')):
                        event.acceptProposedAction()
                        return
        event.ignore()
    
    def dropEvent(self, event):
        """Handle drop event."""
        for url in event.mimeData().urls():
            if url.isLocalFile():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg')):
                    self.audio_section.set_selected_file(file_path)
                    self.on_file_selected(file_path)
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def dragMoveEvent(self, event):
        """Handle drag move event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()