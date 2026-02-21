import sys
import os
from unittest.mock import MagicMock

# Add parent directory to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock heavy dependencies
sys.modules['torch'] = MagicMock()
sys.modules['faster_whisper'] = MagicMock()
sys.modules['ffmpeg'] = MagicMock()
sys.modules['pydub'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['engine'] = MagicMock()
sys.modules['subtitle'] = MagicMock()

# Mock customtkinter classes
class MockCTkBase:
    def __init__(self, master=None, **kwargs):
        pass
    def pack(self, **kwargs):
        pass
    def pack_forget(self):
        pass
    def configure(self, **kwargs):
        pass
    def update_idletasks(self):
        pass
    def set(self, value):
        pass

# We need these to be Classes so inheritance works
class MockCTkFrame(MockCTkBase): pass
class MockCTkLabel(MockCTkBase): pass
class MockCTkProgressBar(MockCTkBase): pass

class MockCTkButton(MockCTkBase):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # We want to verify calls to pack/pack_forget on instances
        self.pack = MagicMock()
        self.pack_forget = MagicMock()
        self._command = kwargs.get('command')

mock_ctk = MagicMock()
mock_ctk.CTkFrame = MockCTkFrame
mock_ctk.CTkLabel = MockCTkLabel
mock_ctk.CTkProgressBar = MockCTkProgressBar
mock_ctk.CTkButton = MockCTkButton

sys.modules['customtkinter'] = mock_ctk
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()

# Import the component to test
try:
    from gui.components import ProgressPanel
except ImportError:
    # Fallback if other modules fail
    sys.modules['gui.app'] = MagicMock()
    from gui.components import ProgressPanel

import unittest
from unittest.mock import patch, call
import platform

class TestProgressPanel(unittest.TestCase):
    def setUp(self):
        self.parent = MagicMock()
        self.panel = ProgressPanel(self.parent)

    def test_complete_shows_button_and_stores_path(self):
        output_path = "/path/to/movie.srt"

        self.panel.complete(success=True, message="Done", output_path=output_path)

        self.assertEqual(self.panel.output_path, output_path)
        self.panel.open_btn.pack.assert_called()
        self.panel.open_btn.pack_forget.assert_not_called()

    def test_complete_failure_hides_button(self):
        self.panel.complete(success=False)
        self.panel.open_btn.pack_forget.assert_called()

    def test_reset_hides_button(self):
        self.panel.output_path = "something"
        self.panel.open_btn.pack_forget.reset_mock()
        self.panel.reset()

        self.assertIsNone(self.panel.output_path)
        self.panel.open_btn.pack_forget.assert_called()

    @patch('gui.components.subprocess.Popen')
    @patch('gui.components.os.startfile', create=True)
    def test_open_file_calls_correct_command(self, mock_startfile, mock_popen):
        self.panel.output_path = "/path/to/file.srt"

        # Test Linux
        with patch('platform.system', return_value='Linux'):
            self.panel._open_file()
            mock_popen.assert_called_with(['xdg-open', "/path/to/file.srt"])

        mock_popen.reset_mock()

        # Test macOS
        with patch('platform.system', return_value='Darwin'):
            self.panel._open_file()
            mock_popen.assert_called_with(['open', "/path/to/file.srt"])

        # Test Windows
        with patch('platform.system', return_value='Windows'):
            self.panel._open_file()
            mock_startfile.assert_called_with("/path/to/file.srt")

if __name__ == '__main__':
    unittest.main()
