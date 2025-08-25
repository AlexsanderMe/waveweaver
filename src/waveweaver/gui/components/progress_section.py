"""
Progress tracking component.
"""

import torch
import numpy as np
from typing import Optional
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QProgressBar, QSizePolicy
from PySide6.QtCore import Qt, QTimer

from ...config.settings import Settings
from ...core.models import ProcessingStatus, AudioFileInfo


class ProgressSection(QFrame):
    """Component for showing processing progress."""
    
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.artificial_progress_timer: Optional[QTimer] = None
        self.current_artificial_progress = 20
        self.audio_duration = 0
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(50)
        
        # Add widgets to layout
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
    
    def start_processing(self):
        """Start processing state."""
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Processing...")
    
    def stop_processing(self):
        """Stop processing state."""
        if self.artificial_progress_timer:
            self.artificial_progress_timer.stop()
            self.artificial_progress_timer = None
        self.progress_bar.setVisible(False)
    
    def update_progress(self, value: int):
        """Update progress bar value."""
        if value > self.progress_bar.value():
            self.progress_bar.setValue(value)
    
    def update_status(self, status: ProcessingStatus):
        """Update status message."""
        status_messages = {
            ProcessingStatus.IDLE: "",
            ProcessingStatus.INITIALIZING: "Initializing...",
            ProcessingStatus.LOADING_MODEL: "Loading model...",
            ProcessingStatus.PROCESSING: "Processing audio...",
            ProcessingStatus.SAVING: "Saving stems...",
            ProcessingStatus.COMPLETED: "Extraction complete!",
            ProcessingStatus.ERROR: "Error occurred!",
            ProcessingStatus.CANCELLED: "Operation cancelled!"
        }
        
        message = status_messages.get(status, "Processing...")
        current_text = self.status_label.text()
        
        # Preserve additional info if present
        if "\n" in current_text:
            lines = current_text.split('\n')
            if len(lines) > 1:
                additional_info = '\n'.join(lines[1:])
                message = f"{message}\n{additional_info}"
        
        self.status_label.setText(message)
    
    def update_device_info(self, device: str):
        """Update device information."""
        current_text = self.status_label.text()
        if "Duration:" in current_text:
            duration_info = current_text.split('\n')[-1]
            self.status_label.setText(f"Processing...\nUsing {device}\n{duration_info}")
        else:
            self.status_label.setText(f"Processing...\nUsing {device}")
    
    def update_audio_info(self, audio_info: AudioFileInfo):
        """Update audio information."""
        self.audio_duration = audio_info.duration
        current_text = self.status_label.text()
        info_text = f"Audio Duration: {audio_info.duration_formatted}"
        
        if "Processing..." in current_text:
            if "Using" in current_text:
                lines = current_text.split('\n')
                self.status_label.setText(f"{lines[0]}\n{lines[1]}\n{info_text}")
            else:
                self.status_label.setText(f"Processing...\n{info_text}")
    
    def start_artificial_progress(self):
        """Start artificial progress animation."""
        is_gpu = torch.cuda.is_available()
        
        self.current_artificial_progress = 15
        
        self.artificial_progress_timer = QTimer()
        self.artificial_progress_timer.timeout.connect(self.update_artificial_progress)
        
        # Calculate interval based on GPU/CPU and duration
        base_interval = 100 if is_gpu else 200
        duration_scale = min((self.audio_duration / 60), 3) ** 0.4
        interval = int(base_interval * duration_scale)
        interval = max(min(interval, 300), 30)
        
        # Add random variation
        variation = interval * 0.3
        interval = int(np.random.uniform(interval - variation, interval + variation))
        
        self.artificial_progress_timer.start(interval)
    
    def update_artificial_progress(self):
        """Update artificial progress."""
        if self.current_artificial_progress < 80:
            min_inc, max_inc = self.calculate_increment_range()
            increment = np.random.uniform(min_inc, max_inc)
            
            self.current_artificial_progress = min(79, self.current_artificial_progress + increment)
            self.progress_bar.setValue(int(self.current_artificial_progress))
    
    def calculate_increment_range(self):
        """Calculate progress increment range based on duration."""
        if self.audio_duration == 0:
            return (0.05, 0.4) if torch.cuda.is_available() else (0.02, 0.2)
        
        duration_factor = (120 / max(self.audio_duration, 1)) ** 1.2
        
        if torch.cuda.is_available():
            min_inc = max(min(0.05 * duration_factor, 0.15), 0.02)
            max_inc = max(min(0.4 * duration_factor, 0.8), 0.2)
        else:
            min_inc = max(min(0.02 * duration_factor, 0.08), 0.01)
            max_inc = max(min(0.2 * duration_factor, 0.4), 0.1)
        
        return (min_inc, max_inc)
    
    def stop_artificial_progress(self):
        """Stop artificial progress and transition to actual progress."""
        if self.artificial_progress_timer:
            self.artificial_progress_timer.stop()
            
            if self.current_artificial_progress < 80:
                transition_timer = QTimer()
                transition_timer.timeout.connect(self.smooth_transition_to_80)
                transition_timer.start(50)
    
    def smooth_transition_to_80(self):
        """Smoothly transition progress to 80%."""
        if self.current_artificial_progress < 80:
            self.current_artificial_progress = min(80, self.current_artificial_progress + 0.5)
            self.progress_bar.setValue(int(self.current_artificial_progress))
        else:
            self.sender().stop()
    
    def show_completion_message(self, message: str):
        """Show completion message."""
        self.status_label.setText(message)
    
    def show_error_message(self, message: str):
        """Show error message."""
        self.status_label.setText(message)