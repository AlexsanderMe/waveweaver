"""
Tests for file handler utilities.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock

from src.waveweaver.utils.file_handler import FileHandler


class TestFileHandler:
    """Test FileHandler class."""
    
    def test_is_audio_file_valid_extensions(self):
        """Test audio file validation with valid extensions."""
        valid_files = [
            "song.mp3",
            "audio.wav", 
            "music.flac",
            "track.m4a",
            "sound.ogg"
        ]
        
        for file_path in valid_files:
            assert FileHandler.is_audio_file(file_path)
    
    def test_is_audio_file_invalid_extensions(self):
        """Test audio file validation with invalid extensions."""
        invalid_files = [
            "document.txt",
            "video.mp4",
            "image.jpg",
            "archive.zip"
        ]
        
        for file_path in invalid_files:
            assert not FileHandler.is_audio_file(file_path)
    
    def test_create_safe_filename(self):
        """Test safe filename creation."""
        unsafe_name = "song<>:\"/\\|?*.mp3"
        safe_name = FileHandler.create_safe_filename(unsafe_name)
        
        assert safe_name == "song.mp3"
    
    def test_create_safe_filename_length_limit(self):
        """Test filename length limiting."""
        long_name = "a" * 100 + ".mp3"
        safe_name = FileHandler.create_safe_filename(long_name, max_length=20)
        
        assert len(safe_name) <= 20
        assert safe_name.endswith(".mp3")
    
    def test_ensure_directory_exists_new_directory(self, tmp_path):
        """Test directory creation."""
        new_dir = tmp_path / "new_folder"
        
        result = FileHandler.ensure_directory_exists(str(new_dir))
        
        assert result is True
        assert new_dir.exists()
    
    def test_ensure_directory_exists_existing_directory(self, tmp_path):
        """Test with existing directory."""
        result = FileHandler.ensure_directory_exists(str(tmp_path))
        
        assert result is True
    
    def test_create_output_filename(self):
        """Test output filename creation."""
        original = "My Song Title.mp3"
        result = FileHandler.create_output_filename(original, "vocals")
        
        assert result == "My Song Title - vocals.wav"
    
    def test_create_output_filename_truncation(self):
        """Test output filename with truncation."""
        original = "Very Long Song Title That Should Be Truncated.mp3"
        result = FileHandler.create_output_filename(original, "vocals", max_length=20)
        
        assert len(result.split(" - ")[0]) <= 23  # Including "..."
        assert result.endswith(" - vocals.wav")