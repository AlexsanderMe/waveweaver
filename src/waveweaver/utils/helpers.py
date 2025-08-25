"""
General helper functions and utilities.
"""

import string
from pathlib import Path
from typing import Union


def truncate_middle(text: str, max_length: int) -> str:
    """
    Truncate text in the middle, keeping start and end visible.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of result
        
    Returns:
        Truncated text with '...' in the middle if needed
    """
    if len(text) <= max_length:
        return text
    
    if max_length <= 3:
        return text[:max_length]
    
    # Calculate characters for each side
    chars_each_side = (max_length - 3) // 2
    
    return f"{text[:chars_each_side]}...{text[-chars_each_side:]}"


def truncate_filename(filename: str, max_length: int) -> str:
    """
    Truncate filename intelligently, preserving word boundaries when possible.
    
    Args:
        filename: Original filename
        max_length: Maximum allowed length
        
    Returns:
        Truncated filename
    """
    if len(filename) <= max_length:
        return filename
    
    # Try to break at word boundaries
    truncated = filename[:max_length].rsplit(' ', 1)[0]
    
    # If breaking at word boundary results in too short text, use simple truncation
    if len(truncated) < max_length // 2:
        truncated = filename[:max_length]
    
    return truncated


def create_safe_filename(filename: str, max_length: int = 50) -> str:
    """
    Create a filesystem-safe filename.
    
    Args:
        filename: Original filename
        max_length: Maximum length allowed
        
    Returns:
        Safe filename with invalid characters removed
    """
    # Define valid characters
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    
    # Remove invalid characters
    safe_filename = ''.join(c for c in filename if c in valid_chars)
    
    # Handle length limit
    if len(safe_filename) > max_length:
        name, ext = Path(safe_filename).stem, Path(safe_filename).suffix
        available_length = max_length - len(ext)
        safe_filename = name[:available_length] + ext
    
    return safe_filename


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to MM:SS format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def validate_audio_file(file_path: Union[str, Path]) -> bool:
    """
    Validate if file is a supported audio format.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if file is valid audio format
    """
    path = Path(file_path)
    supported_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.ogg'}
    
    return (
        path.exists() and
        path.is_file() and
        path.suffix.lower() in supported_extensions
    )


def get_output_folder_name(input_file_path: str) -> str:
    """
    Generate output folder name based on input file.
    
    Args:
        input_file_path: Path to input audio file
        
    Returns:
        Suggested folder name for output
    """
    return Path(input_file_path).stem


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between min and max bounds.
    
    Args:
        value: Value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, t: float) -> float:
    """
    Linear interpolation between two values.
    
    Args:
        start: Start value
        end: End value
        t: Interpolation factor (0.0 to 1.0)
        
    Returns:
        Interpolated value
    """
    return start + t * (end - start)