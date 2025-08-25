"""
Model selection component.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QComboBox, QSizePolicy
from PySide6.QtCore import Signal

from ...config.settings import Settings
from ...core.models import AvailableModels


class ModelSelection(QFrame):
    """Component for AI model selection."""
    
    model_changed = Signal(str)
    
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("Separation Model")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #7aa2f7;")
        
        # Model combo box
        self.model_combo = QComboBox()
        self.model_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Populate combo box
        self.populate_models()
        
        # Connect signal
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.model_combo)
    
    def populate_models(self):
        """Populate the model combo box."""
        models = AvailableModels.get_all_models()
        default_index = 0
        
        for i, (key, model_info) in enumerate(models.items()):
            self.model_combo.addItem(model_info.display_name, key)
            
            # Set default model
            if key == self.settings.model.default_model:
                default_index = i
        
        self.model_combo.setCurrentIndex(default_index)
    
    def on_model_changed(self):
        """Handle model selection change."""
        model_key = self.model_combo.currentData()
        if model_key:
            self.model_changed.emit(model_key)
    
    def get_selected_model(self) -> str:
        """Get the currently selected model key."""
        return self.model_combo.currentData() or self.settings.model.default_model
    
    def set_selected_model(self, model_key: str):
        """Set the selected model by key."""
        for i in range(self.model_combo.count()):
            if self.model_combo.itemData(i) == model_key:
                self.model_combo.setCurrentIndex(i)
                break