"""
Tests for helper functions.
"""

import pytest
from src.waveweaver.utils.helpers import (
    truncate_middle,
    truncate_filename,
    create_safe_filename,
    format_duration,
    format_file_size,
    validate_audio_file,
    clamp,
    lerp
)


class TestHelpers:
    """Test helper functions."""
    
    def test_truncate_middle_short_text(self):
        """Test truncation with text shorter than limit."""
        result = truncate_middle("short", 20)
        assert result == "short"
    
    def test_truncate_middle_long_text(self):
        """Test truncation with text longer than limit."""
        result = truncate_middle("this is a very long text", 15)
        assert len(result) == 15
        assert result.startswith("this")
        assert result.endswith("text")
        assert "..." in result
    
    def test_format_duration(self):
        """Test duration formatting."""
        assert format_duration(65) == "1:05"
        assert format_duration(3661) == "61:01"
        assert format_duration(45.7) == "0:45"
    
    def test_format_file_size(self):
        """Test file size formatting."""
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1536) == "1.5 KB"
        assert format_file_size(1048576) == "1.0 MB"
    
    def test_validate_audio_file_invalid_path(self):
        """Test validation with non-existent file."""
        result = validate_audio_file("nonexistent.mp3")
        assert result is False
    
    def test_clamp(self):
        """Test value clamping."""
        assert clamp(5, 0, 10) == 5
        assert clamp(-1, 0, 10) == 0
        assert clamp(15, 0, 10) == 10
    
    def test_lerp(self):
        """Test linear interpolation."""
        assert lerp(0, 10, 0.5) == 5.0
        assert lerp(0, 10, 0) == 0.0
        assert lerp(0, 10, 1) == 10.0