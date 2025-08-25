"""
Model definitions and data structures.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum


class ProcessingStatus(Enum):
    """Processing status enumeration."""
    IDLE = "idle"
    INITIALIZING = "initializing"
    LOADING_MODEL = "loading_model"
    PROCESSING = "processing"
    SAVING = "saving"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"


@dataclass
class ModelInfo:
    """Information about a Demucs model."""
    key: str
    name: str
    description: str
    stems: List[str]
    
    @property
    def display_name(self) -> str:
        """Get formatted display name."""
        return f"{self.name} - {self.description}"


@dataclass
class AudioFileInfo:
    """Information about an audio file."""
    path: str
    duration: float
    sample_rate: int
    channels: int
    format: str
    
    @property
    def duration_formatted(self) -> str:
        """Get formatted duration string."""
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes}:{seconds:02d}"


@dataclass
class ProcessingResult:
    """Result of stem separation processing."""
    success: bool
    output_files: List[str]
    error_message: str = ""
    processing_time: float = 0.0


class AvailableModels:
    """Registry of available Demucs models."""
    
    MODELS = {
        'htdemucs': ModelInfo(
            key='htdemucs',
            name='HTDemucs',
            description='High quality separation with balanced performance',
            stems=["drums", "bass", "other", "vocals"]
        ),
        'htdemucs_ft': ModelInfo(
            key='htdemucs_ft',
            name='HTDemucs Fine-tuned',
            description='Fine-tuned version with better vocals separation',
            stems=["drums", "bass", "other", "vocals"]
        ),
        'mdx_extra': ModelInfo(
            key='mdx_extra',
            name='MDX-Extra',
            description='High quality separation optimized for vocals',
            stems=["drums", "bass", "other", "vocals"]
        ),
        'mdx_extra_q': ModelInfo(
            key='mdx_extra_q',
            name='MDX-Extra-Q',
            description='Quantized version of MDX-Extra, faster but slightly lower quality',
            stems=["drums", "bass", "other", "vocals"]
        ),
        'htdemucs_6s': ModelInfo(
            key='htdemucs_6s',
            name='HTDemucs 6 Stems',
            description='Separates into 6 stems including piano and guitar',
            stems=["drums", "bass", "other", "vocals", "piano", "guitar"]
        )
    }
    
    @classmethod
    def get_model(cls, key: str) -> ModelInfo:
        """Get model info by key."""
        return cls.MODELS.get(key)
    
    @classmethod
    def get_all_models(cls) -> Dict[str, ModelInfo]:
        """Get all available models."""
        return cls.MODELS.copy()
    
    @classmethod
    def get_model_keys(cls) -> List[str]:
        """Get list of all model keys."""
        return list(cls.MODELS.keys())