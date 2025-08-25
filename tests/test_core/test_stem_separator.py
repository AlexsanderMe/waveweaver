"""
Tests for stem separator.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtCore import QThread

from src.waveweaver.core.stem_separator import StemSeparatorThread
from src.waveweaver.core.models import ProcessingStatus


class TestStemSeparatorThread:
    """Test StemSeparatorThread class."""
    
    @pytest.fixture
    def separator_thread(self, sample_audio_file, output_directory):
        """Create separator thread instance."""
        return StemSeparatorThread(
            input_file=sample_audio_file,
            output_dir=output_directory,
            stems=["vocals", "drums"],
            model_name="htdemucs"
        )
    
    def test_initialization(self, separator_thread, sample_audio_file, output_directory):
        """Test thread initialization."""
        assert separator_thread.input_file == sample_audio_file
        assert separator_thread.output_dir == output_directory
        assert separator_thread.stems == ["vocals", "drums"]
        assert separator_thread.model_name == "htdemucs"
        assert separator_thread.processing_complete is False
    
    def test_cancel(self, separator_thread):
        """Test cancellation."""
        separator_thread.cancel()
        assert separator_thread._is_cancelled is True
    
    @patch('src.waveweaver.core.stem_separator.sf.info')
    def test_get_audio_info_success(self, mock_sf_info, separator_thread):
        """Test audio info retrieval."""
        # Mock soundfile info
        mock_info = Mock()
        mock_info.duration = 120.5
        mock_info.samplerate = 44100
        mock_info.channels = 2
        mock_info.format = "WAV"
        mock_sf_info.return_value = mock_info
        
        audio_info = separator_thread._get_audio_info()
        
        assert audio_info.duration == 120.5
        assert audio_info.sample_rate == 44100
        assert audio_info.channels == 2
        assert audio_info.format == "WAV"
    
    @patch('src.waveweaver.core.stem_separator.sf.info')
    def test_get_audio_info_error(self, mock_sf_info, separator_thread):
        """Test audio info retrieval with error."""
        mock_sf_info.side_effect = Exception("File error")
        
        audio_info = separator_thread._get_audio_info()
        
        assert audio_info.duration == 0
        assert audio_info.sample_rate == 44100  # Default
        assert audio_info.channels == 2  # Default