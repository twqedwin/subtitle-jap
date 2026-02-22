import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Mock dependencies
class MockWidget(MagicMock):
    def __init__(self, master=None, **kwargs):
        super().__init__()
        self.master = master
        self.pack = MagicMock()
        self.pack_forget = MagicMock()
        self.configure = MagicMock()
        self.browse_btn = MagicMock()

class MockCTk:
    def __init__(self, **kwargs):
        pass
    def geometry(self, *args): pass
    def resizable(self, *args): pass
    def title(self, *args): pass
    def after(self, *args): pass
    def mainloop(self): pass
    def configure(self, *args, **kwargs): pass

mock_ctk = MagicMock()
mock_ctk.CTk = MockCTk
mock_ctk.CTkFrame = MockWidget
mock_ctk.CTkButton = MockWidget
mock_ctk.CTkLabel = MockWidget
mock_ctk.CTkProgressBar = MockWidget
mock_ctk.set_appearance_mode = MagicMock()
mock_ctk.set_default_color_theme = MagicMock()

sys.modules["customtkinter"] = mock_ctk
sys.modules["tkinter"] = MagicMock()
sys.modules["tkinter.messagebox"] = MagicMock()
sys.modules["engine"] = MagicMock()
sys.modules["subtitle"] = MagicMock()
sys.modules["gui.components"] = MagicMock()
from gui.components import DropZone, ProgressPanel

# Re-mock DropZone and ProgressPanel to return MockWidgets
sys.modules["gui.components"].DropZone = MockWidget
sys.modules["gui.components"].ProgressPanel = MockWidget

# Now import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gui.app import SubtitleGeneratorApp

class TestOpenFolderLogic(unittest.TestCase):
    def setUp(self):
        # Instantiate app
        self.app = SubtitleGeneratorApp()
        # Mock internal buttons if they weren't created by _build_ui (depends on implementation state)
        if not hasattr(self.app, 'open_folder_btn'):
            self.app.open_folder_btn = MockWidget()

        # Ensure other buttons are mocks so we can check calls
        if not isinstance(self.app.start_btn, MagicMock):
             self.app.start_btn = MockWidget()

    def test_open_output_folder_method_exists(self):
        """Test that _open_output_folder method exists."""
        self.assertTrue(hasattr(self.app, "_open_output_folder"), "Method _open_output_folder should exist")

    def test_open_folder_windows(self):
        """Test logic for opening folder on Windows."""
        if not hasattr(self.app, "_open_output_folder"):
            return

        with patch("platform.system", return_value="Windows"):
            with patch("os.startfile", create=True) as mock_startfile:
                # Use forward slashes to be compatible with PosixPath in tests running on Linux
                self.app.last_output_path = "C:/Users/Test/Video/movie.srt"
                self.app._open_output_folder()
                # Should open the directory
                mock_startfile.assert_called_with("C:/Users/Test/Video")

    def test_open_folder_mac(self):
        """Test logic for opening folder on macOS."""
        if not hasattr(self.app, "_open_output_folder"):
            return

        with patch("platform.system", return_value="Darwin"):
            with patch("subprocess.call") as mock_call:
                self.app.last_output_path = "/Users/Test/Video/movie.srt"
                self.app._open_output_folder()
                # Should open the directory
                mock_call.assert_called_with(["open", "/Users/Test/Video"])

    def test_open_folder_linux(self):
        """Test logic for opening folder on Linux."""
        if not hasattr(self.app, "_open_output_folder"):
            return

        with patch("platform.system", return_value="Linux"):
            with patch("subprocess.call") as mock_call:
                self.app.last_output_path = "/home/test/video/movie.srt"
                self.app._open_output_folder()
                # Should open the directory
                mock_call.assert_called_with(["xdg-open", "/home/test/video"])

    def test_on_success_updates_ui(self):
        """Test that _on_success reveals the button."""
        if not hasattr(self.app, "_on_success"):
            return

        output_path = "/path/to/output.srt"
        self.app._on_success(output_path)

        self.assertEqual(self.app.last_output_path, output_path)
        # Check if button is packed (visible)
        self.app.open_folder_btn.pack.assert_called()

    def test_start_processing_resets_ui(self):
        """Test that _start_processing hides the button."""
        if not hasattr(self.app, "_start_processing"):
            return

        # Setup mocks
        self.app.current_file = "test.mp4"
        self.app.progress_panel = MagicMock()
        self.app.start_btn = MagicMock()
        self.app.cancel_btn = MagicMock()
        self.app.drop_zone = MagicMock()
        self.app.open_folder_btn = MagicMock()

        # Mock threading to avoid starting thread
        with patch("threading.Thread"):
             self.app._start_processing()

        self.app.open_folder_btn.pack_forget.assert_called()
        self.assertIsNone(self.app.last_output_path)

if __name__ == "__main__":
    unittest.main()
