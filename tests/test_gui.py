import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock modules before import
class MockCTk:
    def __init__(self, *args, **kwargs):
        pass
    def title(self, *args, **kwargs): pass
    def geometry(self, *args, **kwargs): pass
    def resizable(self, *args, **kwargs): pass
    def pack(self, *args, **kwargs): pass
    def after(self, *args, **kwargs): pass
    def configure(self, *args, **kwargs): pass
    def mainloop(self, *args, **kwargs): pass
    def update_idletasks(self, *args, **kwargs): pass
    def set(self, *args, **kwargs): pass
    def pack_forget(self, *args, **kwargs): pass

mock_ctk = MagicMock()
mock_ctk.CTk = MockCTk
mock_ctk.CTkFrame = MockCTk
mock_ctk.CTkLabel = MockCTk
mock_ctk.CTkButton = MockCTk
mock_ctk.CTkProgressBar = MockCTk

mock_tkinter = MagicMock()
mock_engine = MagicMock()
mock_subtitle = MagicMock()

sys.modules['customtkinter'] = mock_ctk
sys.modules['tkinter'] = mock_tkinter
sys.modules['engine'] = mock_engine
sys.modules['subtitle'] = mock_subtitle

# Now we can safely import gui
from gui.utils import open_file_explorer
from gui.app import SubtitleGeneratorApp
import platform

class TestGuiUtils(unittest.TestCase):
    @patch('gui.utils.subprocess.Popen')
    @patch('gui.utils.platform.system')
    def test_open_file_explorer_windows(self, mock_system, mock_popen):
        mock_system.return_value = "Windows"
        open_file_explorer("test/path.srt")
        mock_popen.assert_called_once_with(["explorer", "/select,", "test/path.srt"])

    @patch('gui.utils.subprocess.Popen')
    @patch('gui.utils.platform.system')
    def test_open_file_explorer_mac(self, mock_system, mock_popen):
        mock_system.return_value = "Darwin"
        open_file_explorer("test/path.srt")
        mock_popen.assert_called_once_with(["open", "-R", "test/path.srt"])

    @patch('gui.utils.subprocess.Popen')
    @patch('gui.utils.platform.system')
    def test_open_file_explorer_linux(self, mock_system, mock_popen):
        mock_system.return_value = "Linux"
        open_file_explorer("test/path.srt")
        mock_popen.assert_called_once_with(["xdg-open", "test"])

class TestApp(unittest.TestCase):
    @patch('gui.app.open_file_explorer')
    def test_show_success_ui(self, mock_open_file):
        app = SubtitleGeneratorApp()
        app.start_btn = MagicMock()
        app.cancel_btn = MagicMock()
        app.open_btn = MagicMock()
        app.drop_zone = MagicMock()

        # Test UI state update
        app._show_success_ui("output.srt")

        # Check that widgets are unpacked and repacked to maintain order
        app.start_btn.pack_forget.assert_called()
        app.cancel_btn.pack_forget.assert_called()

        # Order assertion:
        self.assertEqual(app.start_btn.pack.call_count, 1)
        self.assertEqual(app.cancel_btn.pack.call_count, 1)
        self.assertEqual(app.open_btn.pack.call_count, 1)

if __name__ == '__main__':
    unittest.main()
