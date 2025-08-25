"""
File handling utilities.
"""

import os
import string
from pathlib import Path
from typing import List, Optional, Tuple


class FileHandler:
    """Utilities for file operations."""
    
    SUPPORTED_AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.m4a', '.ogg'}
    
    @classmethod
    def is_audio_file(cls, file_path: str) -> bool:
        """Check if file is a supported audio format."""
        return Path(file_path).suffix.lower() in cls.SUPPORTED_AUDIO_EXTENSIONS
    
    @classmethod
    def get_audio_files_from_urls(cls, urls) -> List[str]:
        """Extract valid audio file paths from dropped URLs."""
        audio_files = []
        for url in urls:
            if url.isLocalFile():
                file_path = url.toLocalFile()
                if cls.is_audio_file(file_path):
                    audio_files.append(file_path)
        return audio_files
    
    @classmethod
    def create_safe_filename(cls, filename: str, max_length: int = 50) -> str:
        """Create a safe filename by removing invalid characters."""
        # Define valid characters
        valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
        
        # Remove invalid characters
        safe_filename = ''.join(c for c in filename if c in valid_chars)
        
        # Limit length
        if len(safe_filename) > max_length:
            name, ext = os.path.splitext(safe_filename)
            safe_filename = name[:max_length - len(ext)] + ext
        
        return safe_filename
    
    @classmethod
    def ensure_directory_exists(cls, directory_path: str) -> bool:
        """Ensure directory exists, create if it doesn't."""
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @classmethod
    def get_file_info(cls, file_path: str) -> Optional[Tuple[str, int]]:
        """Get basic file information."""
        try:
            path = Path(file_path)
            if path.exists():
                return path.name, path.stat().st_size
        except Exception:
            pass
        return None
    
    @classmethod
    def create_output_filename(cls, original_filename: str, stem: str, 
                             max_length: int = 25) -> str:
        """Create output filename for a stem."""
        base_name = Path(original_filename).stem
        
        # Truncate if too long
        if len(base_name) > max_length:
            # Try to split at word boundary
            truncated = base_name[:max_length].rsplit(' ', 1)[0]
            if len(truncated) < max_length // 2:  # If split too aggressively
                truncated = base_name[:max_length]
            base_name = truncated + '...'
        
        return f"{base_name} - {stem}.wav"
    
    @classmethod
    def get_available_filename(cls, file_path: str) -> str:
        """Get an available filename by adding numbers if needed."""
        path = Path(file_path)
        if not path.exists():
            return file_path
        
        base = path.stem
        suffix = path.suffix
        parent = path.parent
        counter = 1
        
        while True:
            new_name = f"{base} ({counter}){suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return str(new_path)
            counter += 1