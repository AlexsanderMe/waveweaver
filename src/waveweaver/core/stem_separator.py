"""
Core stem separation logic using Demucs.
"""

import os
import time
import warnings
from pathlib import Path
from typing import List, Callable, Optional

import torch
import soundfile as sf
import numpy as np
from PySide6.QtCore import QThread, Signal

from demucs.apply import apply_model
from demucs.audio import AudioFile
from demucs.pretrained import get_model

from .models import ProcessingStatus, ProcessingResult, AudioFileInfo, AvailableModels
from ..utils.file_handler import FileHandler
from ..utils.helpers import create_safe_filename, truncate_filename


class StemSeparatorThread(QThread):
    """Thread for handling stem separation processing."""
    
    # Signals
    progress = Signal(int)
    status_changed = Signal(ProcessingStatus)
    error = Signal(str)
    finished = Signal(ProcessingResult)
    device_info = Signal(str)
    audio_info = Signal(AudioFileInfo)
    artificial_progress_finished = Signal()
    
    def __init__(self, input_file: str, output_dir: str, 
                 stems: List[str], model_name: str):
        super().__init__()
        self.input_file = input_file
        self.output_dir = output_dir
        self.stems = stems
        self.model_name = model_name
        self.processing_complete = False
        self.start_time = 0
        self._is_cancelled = False
        
    def run(self):
        """Main processing thread."""
        try:
            self.start_time = time.time()
            warnings.filterwarnings("ignore")
            
            # Get audio file info
            audio_info = self._get_audio_info()
            self.audio_info.emit(audio_info)
            self.progress.emit(5)
            
            # Load model
            self.status_changed.emit(ProcessingStatus.LOADING_MODEL)
            model = self._load_model()
            self.progress.emit(10)
            
            # Emit device info
            device_name = self._get_device_name()
            self.device_info.emit(device_name)
            
            # Load and prepare audio
            self.status_changed.emit(ProcessingStatus.PROCESSING)
            wav, sample_rate = self._load_audio()
            self.progress.emit(15)
            
            if self._is_cancelled:
                return
            
            # Apply model
            sources = self._apply_separation(model, wav)
            self.processing_complete = True
            self.artificial_progress_finished.emit()
            self.progress.emit(80)
            
            if self._is_cancelled:
                return
            
            # Save stems
            self.status_changed.emit(ProcessingStatus.SAVING)
            output_files = self._save_stems(sources, sample_rate)
            self.progress.emit(100)
            
            # Emit success
            processing_time = time.time() - self.start_time
            result = ProcessingResult(
                success=True,
                output_files=output_files,
                processing_time=processing_time
            )
            self.status_changed.emit(ProcessingStatus.COMPLETED)
            self.finished.emit(result)
            
        except Exception as e:
            error_msg = str(e)
            self.error.emit(error_msg)
            result = ProcessingResult(
                success=False,
                output_files=[],
                error_message=error_msg
            )
            self.status_changed.emit(ProcessingStatus.ERROR)
            self.finished.emit(result)
    
    def cancel(self):
        """Cancel the processing."""
        self._is_cancelled = True
        self.status_changed.emit(ProcessingStatus.CANCELLED)
    
    def _get_audio_info(self) -> AudioFileInfo:
        """Get information about the audio file."""
        try:
            info = sf.info(self.input_file)
            return AudioFileInfo(
                path=self.input_file,
                duration=info.duration,
                sample_rate=info.samplerate,
                channels=info.channels,
                format=info.format
            )
        except Exception:
            return AudioFileInfo(
                path=self.input_file,
                duration=0,
                sample_rate=44100,
                channels=2,
                format="unknown"
            )
    
    def _load_model(self):
        """Load the Demucs model."""
        model = get_model(self.model_name)
        if torch.cuda.is_available():
            model.cuda()
        else:
            model.cpu()
        return model
    
    def _get_device_name(self) -> str:
        """Get the processing device name."""
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            return f'GPU - {gpu_name}'
        else:
            return 'CPU'
    
    def _load_audio(self):
        """Load and prepare audio for processing."""
        audio_file = AudioFile(self.input_file)
        wav = audio_file.read()
        sample_rate = audio_file.samplerate()
        
        if wav.dim() == 1:
            wav = wav.unsqueeze(0)
        
        return wav, sample_rate
    
    def _apply_separation(self, model, wav):
        """Apply the model for stem separation."""
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        sources = apply_model(
            model, 
            wav, 
            device=device,
            progress=False,
            shifts=2
        )
        return sources.cpu()
    
    def _save_stems(self, sources, sample_rate) -> List[str]:
        """Save the separated stems to files."""
        # Create output folder
        base_name = Path(self.input_file).stem
        output_folder = Path(self.output_dir) / base_name
        output_folder.mkdir(exist_ok=True)
        
        # Get stem names for the model
        model_info = AvailableModels.get_model(self.model_name)
        stem_names = model_info.stems
        
        output_files = []
        progress_per_stem = 20 / len(self.stems)
        current_progress = 80
        
        for stem in self.stems:
            if self._is_cancelled:
                break
                
            # Find the correct stem index
            stem_index = stem_names.index(stem)
            
            # Create safe filename
            original_name = Path(self.input_file).stem
            truncated_name = truncate_filename(original_name, 25)
            output_file = output_folder / f"{truncated_name} - {stem}.wav"
            
            # Save stem
            stem_audio = sources[0, stem_index].numpy()
            sf.write(str(output_file), stem_audio.T, sample_rate)
            
            output_files.append(str(output_file))
            current_progress += progress_per_stem
            self.progress.emit(int(current_progress))
        
        return output_files