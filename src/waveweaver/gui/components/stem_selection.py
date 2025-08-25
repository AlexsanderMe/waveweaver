"""
Stem selection component.
"""

from typing import List, Dict
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QCheckBox, QSizePolicy

from ...config.settings import Settings


class StemSelection(QFrame):
    """Component for selecting stems to extract."""
    
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.stem_checkboxes: Dict[str, QCheckBox] = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        
        # Title
        self.title_label = QLabel("Stems to Extract")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #7aa2f7;")
        self.layout.addWidget(self.title_label)
    
    def update_stems(self, stems: List[str]):
        """Update the available stems based on selected model."""
        # Clear existing checkboxes
        self.clear_stems()
        
        # Add new checkboxes
        for stem in stems:
            checkbox = QCheckBox(stem.capitalize())
            checkbox.setChecked(True)  # Default to all selected
            self.stem_checkboxes[stem] = checkbox
            self.layout.addWidget(checkbox)
    
    def clear_stems(self):
        """Clear all stem checkboxes."""
        for checkbox in self.stem_checkboxes.values():
            self.layout.removeWidget(checkbox)
            checkbox.deleteLater()
        self.stem_checkboxes.clear()
    
    def get_selected_stems(self) -> List[str]:
        """Get list of selected stems."""
        return [
            stem for stem, checkbox in self.stem_checkboxes.items()
            if checkbox.isChecked()
        ]
    
    def select_all_stems(self):
        """Select all available stems."""
        for checkbox in self.stem_checkboxes.values():
            checkbox.setChecked(True)
    
    def deselect_all_stems(self):
        """Deselect all stems."""
        for checkbox in self.stem_checkboxes.values():
            checkbox.setChecked(False)
    
    def set_stem_selection(self, stem: str, selected: bool):
        """Set selection state for a specific stem."""
        if stem in self.stem_checkboxes:
            self.stem_checkboxes[stem].setChecked(selected)
    
    def is_stem_selected(self, stem: str) -> bool:
        """Check if a specific stem is selected."""
        return (
            stem in self.stem_checkboxes and 
            self.stem_checkboxes[stem].isChecked()
        )