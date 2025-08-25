"""
Pytest configuration and fixtures.
"""

import pytest
from unittest.mock import MagicMock
from pathlib import Path
from PySide6.QtWidgets import QApplication
import sys

# Adiciona o diretório src ao path para importar módulos do projeto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from waveweaver.config.settings import Settings


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for GUI tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    if app:
        app.quit()


@pytest.fixture
def settings():
    """Create test settings instance."""
    return Settings()


@pytest.fixture
def sample_audio_file(tmp_path):
    """Create a sample audio file for testing."""
    audio_file = tmp_path / "sample.wav"
    audio_file.write_bytes(b"fake audio content")
    return str(audio_file)


@pytest.fixture
def output_directory(tmp_path):
    """Create temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return str(output_dir)