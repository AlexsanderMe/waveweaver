"""
Tests for main window.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QUrl, QMimeData
from PySide6.QtGui import QDropEvent, QDragEnterEvent

import sys
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from waveweaver.gui.main_window import MainWindow
from waveweaver.config.settings import Settings
from waveweaver.core.models import ProcessingResult, AvailableModels


class TestMainWindow:
    """Test MainWindow class."""
   
    @pytest.fixture
    def main_window(self, qapp, settings):
        """Create main window instance."""
        return MainWindow(settings)
   
    def test_initialization(self, main_window, settings):
        """Test main window initialization."""
        assert main_window.settings == settings
        assert main_window.input_file is None
        assert main_window.output_dir is None
        assert main_window.separator_thread is None
        assert main_window.artificial_progress_timer is None
        assert main_window.current_artificial_progress == 20
   
    def test_window_properties(self, main_window, settings):
        """Test window properties."""
        assert main_window.windowTitle() == "WaveWeaver"
        assert main_window.minimumWidth() == settings.window.min_width
        assert main_window.minimumHeight() == settings.window.min_height
        assert main_window.width() == settings.window.width
        assert main_window.height() == settings.window.height
    
    def test_window_accepts_drops(self, main_window):
        """Test window accepts drag and drop."""
        assert main_window.acceptDrops() is True
    
    def test_ui_components_creation(self, main_window):
        """Test UI components are created."""
        assert hasattr(main_window, 'audio_section')
        assert hasattr(main_window, 'model_selection')
        assert hasattr(main_window, 'progress_section')
        assert hasattr(main_window, 'stem_selection')
        assert hasattr(main_window, 'output_section')
        assert hasattr(main_window, 'extract_btn')
        assert hasattr(main_window, 'cancel_btn')
    
    def test_extract_button_initial_state(self, main_window):
        """Test extract button initial state."""
        assert main_window.extract_btn.isEnabled() is False
        assert main_window.extract_btn.text() == "Extract Stems"
    
    def test_cancel_button_initial_state(self, main_window):
        """Test cancel button initial state."""
        assert main_window.cancel_btn.isVisible() is False
        assert main_window.cancel_btn.text() == "Force Cancel"
    
    def test_on_file_selected(self, main_window):
        """Test file selection handler."""
        test_file = "/path/to/test.mp3"
        
        main_window.on_file_selected(test_file)
        
        assert main_window.input_file == test_file
    
    def test_on_output_folder_selected(self, main_window):
        """Test output folder selection handler."""
        test_folder = "/path/to/output"
        
        main_window.on_output_folder_selected(test_folder)
        
        assert main_window.output_dir == test_folder
    
    def test_update_extract_button_state_enabled(self, main_window):
        """Test extract button enabled when conditions are met."""
        main_window.input_file = "/path/to/test.mp3"
        main_window.output_dir = "/path/to/output"
        main_window.separator_thread = None
        
        main_window.update_extract_button_state()
        
        assert main_window.extract_btn.isEnabled() is True
    
    def test_update_extract_button_state_disabled_no_input(self, main_window):
        """Test extract button disabled when no input file."""
        main_window.input_file = None
        main_window.output_dir = "/path/to/output"
        main_window.separator_thread = None
        
        main_window.update_extract_button_state()
        
        assert main_window.extract_btn.isEnabled() is False
    
    def test_update_extract_button_state_disabled_no_output(self, main_window):
        """Test extract button disabled when no output directory."""
        main_window.input_file = "/path/to/test.mp3"
        main_window.output_dir = None
        main_window.separator_thread = None
        
        main_window.update_extract_button_state()
        
        assert main_window.extract_btn.isEnabled() is False
    
    def test_update_extract_button_state_disabled_thread_running(self, main_window):
        """Test extract button disabled when thread is running."""
        main_window.input_file = "/path/to/test.mp3"
        main_window.output_dir = "/path/to/output"
        main_window.separator_thread = Mock()
        
        main_window.update_extract_button_state()
        
        assert main_window.extract_btn.isEnabled() is False
    
    @patch('waveweaver.gui.main_window.StemSeparatorThread')
    def test_start_extraction_success(self, mock_thread_class, main_window):
        """Test successful extraction start."""
        # Setup
        main_window.input_file = "/path/to/test.mp3"
        main_window.output_dir = "/path/to/output"
        main_window.stem_selection.get_selected_stems = Mock(return_value=['vocals', 'drums'])
        main_window.model_selection.get_selected_model = Mock(return_value='htdemucs_ft')
        main_window.progress_section.start_processing = Mock()
        
        mock_thread = Mock()
        mock_thread_class.return_value = mock_thread
        
        # Use patch.object para espionar o método setVisible do botão
        with patch.object(main_window.cancel_btn, 'setVisible') as mock_set_visible:
            # Execute
            main_window.start_extraction()
            
            # Verify
            mock_thread_class.assert_called_once()
            main_window.progress_section.start_processing.assert_called_once()
            assert main_window.extract_btn.isEnabled() is False
            
            # Verifique se setVisible(True) foi chamado no botão de cancelar
            mock_set_visible.assert_called_once_with(True)
            
            assert main_window.separator_thread == mock_thread
            mock_thread.start.assert_called_once()
    
    @patch('waveweaver.gui.main_window.QMessageBox')
    def test_start_extraction_no_stems_selected(self, mock_msg_box, main_window):
        """Test extraction start with no stems selected."""
        # Setup
        main_window.input_file = "/path/to/test.mp3"
        main_window.output_dir = "/path/to/output"
        main_window.stem_selection.get_selected_stems = Mock(return_value=[])
        
        # Execute
        main_window.start_extraction()
        
        # Verify
        mock_msg_box.warning.assert_called_once()
        assert main_window.separator_thread is None
    
    def test_start_extraction_no_input_file(self, main_window):
        """Test extraction start with no input file."""
        main_window.input_file = None
        main_window.output_dir = "/path/to/output"
        
        main_window.start_extraction()
        
        assert main_window.separator_thread is None
    
    def test_start_extraction_no_output_dir(self, main_window):
        """Test extraction start with no output directory."""
        main_window.input_file = "/path/to/test.mp3"
        main_window.output_dir = None
        
        main_window.start_extraction()
        
        assert main_window.separator_thread is None
    
    @patch('waveweaver.gui.main_window.QMessageBox')
    def test_handle_error(self, mock_msg_box, main_window):
        """Test error handling."""
        error_msg = "Test error message"
        
        main_window.handle_error(error_msg)
        
        mock_msg_box.critical.assert_called_once_with(
            main_window, "Error", f"An error occurred: {error_msg}"
        )
    
    def test_on_extraction_complete_success(self, main_window):
        """Test successful extraction completion."""
        # Setup
        main_window.progress_section.stop_processing = Mock()
        main_window.progress_section.show_completion_message = Mock()
        main_window.separator_thread = Mock()
        
        result = ProcessingResult(success=True, output_files=[], processing_time=10.5)
        
        # Execute
        main_window.on_extraction_complete(result)
        
        # Verify
        main_window.progress_section.stop_processing.assert_called_once()
        main_window.progress_section.show_completion_message.assert_called_once_with(
            "Extraction complete! (10.5s)"
        )
        assert main_window.extract_btn.isEnabled() is True
        assert main_window.cancel_btn.isVisible() is False
    
    def test_on_extraction_complete_failure(self, main_window):
        """Test failed extraction completion."""
        # Setup
        main_window.progress_section.stop_processing = Mock()
        main_window.progress_section.show_error_message = Mock()
        main_window.separator_thread = Mock()
        
        result = ProcessingResult(success=False, output_files=[], error_message="Test error")
        
        # Execute
        main_window.on_extraction_complete(result)
        
        # Verify
        main_window.progress_section.stop_processing.assert_called_once()
        main_window.progress_section.show_error_message.assert_called_once_with(
            "Extraction failed!"
        )
        assert main_window.extract_btn.isEnabled() is True
        assert main_window.cancel_btn.isVisible() is False
    
    def test_on_model_changed(self, main_window):
        """Test model change handler."""
        # Setup
        model_key = "htdemucs_ft"
        main_window.stem_selection.update_stems = Mock()
        
        # Execute
        main_window.on_model_changed(model_key)
        
        # Verify
        model_info = AvailableModels.get_model(model_key)
        main_window.stem_selection.update_stems.assert_called_once_with(model_info.stems)
    
    def test_drag_enter_event_valid_audio_file(self, main_window):
        """Test drag enter event with valid audio file."""
        # Create mock event
        mock_event = Mock()
        mock_mime_data = Mock()
        mock_url = Mock()
        mock_url.isLocalFile.return_value = True
        mock_url.toLocalFile.return_value = "/path/to/test.mp3"
        mock_mime_data.hasUrls.return_value = True
        mock_mime_data.urls.return_value = [mock_url]
        mock_event.mimeData.return_value = mock_mime_data
        
        # Execute
        main_window.dragEnterEvent(mock_event)
        
        # Verify
        mock_event.acceptProposedAction.assert_called_once()
    
    def test_drag_enter_event_invalid_file(self, main_window):
        """Test drag enter event with invalid file."""
        # Create mock event
        mock_event = Mock()
        mock_mime_data = Mock()
        mock_url = Mock()
        mock_url.isLocalFile.return_value = True
        mock_url.toLocalFile.return_value = "/path/to/test.txt"
        mock_mime_data.hasUrls.return_value = True
        mock_mime_data.urls.return_value = [mock_url]
        mock_event.mimeData.return_value = mock_mime_data
        
        # Execute
        main_window.dragEnterEvent(mock_event)
        
        # Verify
        mock_event.ignore.assert_called_once()
    
    def test_drop_event_valid_audio_file(self, main_window):
        """Test drop event with valid audio file."""
        # Setup
        test_file = "/path/to/test.wav"
        main_window.audio_section.set_selected_file = Mock()
        
        # Create mock event
        mock_event = Mock()
        mock_mime_data = Mock()
        mock_url = Mock()
        mock_url.isLocalFile.return_value = True
        mock_url.toLocalFile.return_value = test_file
        mock_mime_data.urls.return_value = [mock_url]
        mock_event.mimeData.return_value = mock_mime_data
        
        # Execute
        main_window.dropEvent(mock_event)
        
        # Verify
        main_window.audio_section.set_selected_file.assert_called_once_with(test_file)
        assert main_window.input_file == test_file
        mock_event.acceptProposedAction.assert_called_once()
    
    def test_drop_event_invalid_file(self, main_window):
        """Test drop event with invalid file."""
        # Create mock event
        mock_event = Mock()
        mock_mime_data = Mock()
        mock_url = Mock()
        mock_url.isLocalFile.return_value = True
        mock_url.toLocalFile.return_value = "/path/to/test.doc"
        mock_mime_data.urls.return_value = [mock_url]
        mock_event.mimeData.return_value = mock_mime_data
        
        # Execute
        main_window.dropEvent(mock_event)
        
        # Verify
        mock_event.ignore.assert_called_once()
    
    @patch('waveweaver.gui.main_window.QMessageBox')
    def test_close_event_with_running_process_cancel(self, mock_msg_box, main_window):
        """Test close event with running process - user cancels."""
        # Setup
        mock_event = Mock()
        main_window.separator_thread = Mock()
        mock_msg_box.warning.return_value = mock_msg_box.StandardButton.No
        
        # Execute
        main_window.closeEvent(mock_event)
        
        # Verify
        mock_msg_box.warning.assert_called_once()
        mock_event.ignore.assert_called_once()
    
    @patch('waveweaver.gui.main_window.QMessageBox')
    def test_close_event_with_running_process_accept(self, mock_msg_box, main_window):
        """Test close event with running process - user accepts."""
        # Setup
        mock_event = Mock()
        main_window.separator_thread = Mock()
        mock_msg_box.warning.return_value = mock_msg_box.StandardButton.Yes
        
        # Execute
        main_window.closeEvent(mock_event)
        
        # Verify
        mock_msg_box.warning.assert_called_once()
        mock_event.accept.assert_called_once()
    
    def test_close_event_no_running_process(self, main_window):
        """Test close event with no running process."""
        # Setup
        mock_event = Mock()
        main_window.separator_thread = None
        
        # Execute
        main_window.closeEvent(mock_event)
        
        # Verify
        mock_event.accept.assert_called_once()
    
    def test_resize_event(self, main_window):
        """Test window resize event."""
        from PySide6.QtGui import QResizeEvent
        from PySide6.QtCore import QSize
        # Setup
        old_size = QSize(800, 600)
        new_size = QSize(1000, 700)
        event = QResizeEvent(new_size, old_size)
        
        # Execute
        main_window.resizeEvent(event)
        
        # Verify - columns should be resized
        expected_width = int(1000 * 0.45)  # 450
        assert main_window._left_widget.maximumWidth() == expected_width
        assert main_window._right_widget.maximumWidth() == expected_width
    
    @patch('waveweaver.gui.main_window.QMessageBox')
    def test_force_cancel_user_accepts(self, mock_msg_box, main_window):
        """Test force cancel when user accepts."""
        # Setup
        main_window.separator_thread = Mock()
        mock_msg_box.warning.return_value = mock_msg_box.StandardButton.Yes
        
        with patch.object(main_window, '_restart_application') as mock_restart:
            # Execute
            main_window.force_cancel()
            
            # Verify
            mock_msg_box.warning.assert_called_once()
            mock_restart.assert_called_once()
    
    @patch('waveweaver.gui.main_window.QMessageBox')
    def test_force_cancel_user_rejects(self, mock_msg_box, main_window):
        """Test force cancel when user rejects."""
        # Setup
        main_window.separator_thread = Mock()
        mock_msg_box.warning.return_value = mock_msg_box.StandardButton.No
        
        with patch.object(main_window, '_restart_application') as mock_restart:
            # Execute
            main_window.force_cancel()
            
            # Verify
            mock_msg_box.warning.assert_called_once()
            mock_restart.assert_not_called()
    
    def test_force_cancel_no_thread(self, main_window):
        """Test force cancel with no running thread."""
        main_window.separator_thread = None
        
        with patch.object(main_window, '_restart_application') as mock_restart:
            main_window.force_cancel()
            mock_restart.assert_not_called()