import unittest
import sys
from unittest.mock import MagicMock, patch

# Mock customtkinter and tkinter
class MockCTk:
    def __init__(self, *args, **kwargs):
        pass
    def title(self, *args): pass
    def geometry(self, *args): pass
    def resizable(self, *args): pass
    def pack(self, *args, **kwargs): pass
    def mainloop(self): pass
    def after(self, delay, callback): callback()

mock_ctk = MagicMock()
mock_ctk.CTk = MockCTk
mock_ctk.set_appearance_mode = MagicMock()
mock_ctk.set_default_color_theme = MagicMock()

mock_tkinter = MagicMock()

# We only mock what we must. engine and subtitle don't necessarily need full mock if we patch their usage,
# but memory says: "Unit testing gui modules requires mocking customtkinter, tkinter, engine, and subtitle in sys.modules before import. Specifically, to mock ctk.CTk for inheritance, assign a dummy class (e.g., class MockCTk: pass) to mock_ctk.CTk instead of using a standard MagicMock."
import sys

# Store original modules
_original_modules = {k: sys.modules.get(k) for k in ['customtkinter', 'tkinter', 'engine', 'subtitle']}

sys.modules['customtkinter'] = mock_ctk
sys.modules['tkinter'] = mock_tkinter
sys.modules['engine'] = MagicMock()
sys.modules['subtitle'] = MagicMock()

import gui.app
from gui.app import SubtitleGeneratorApp

class TestApp(unittest.TestCase):

    def tearDown(self):
        for k, v in _original_modules.items():
            if v is None:
                if k in sys.modules:
                    del sys.modules[k]
            else:
                sys.modules[k] = v

    @patch('gui.app.threading.Thread')
    @patch('gui.app.get_output_path')
    @patch('gui.app.generate_srt')
    @patch('gui.app.JapaneseTranscriber')
    def test_process_video_skips_extraction(self, MockTranscriber, mock_generate_srt, mock_get_output_path, mock_thread):
        app = SubtitleGeneratorApp()
        app.current_file = "test_video.mkv"

        # Override the transcriber with our mock
        mock_transcriber_instance = MagicMock()
        mock_transcriber_instance.transcribe.return_value = [{"start": 0, "end": 1, "text": "test"}]
        app.transcriber = mock_transcriber_instance

        mock_get_output_path.return_value = "test_video.srt"

        # Call _process_video directly to bypass threading for synchronous testing
        app._process_video()

        # Check that it transcribes the video file directly
        mock_transcriber_instance.transcribe.assert_called_once_with("test_video.mkv")

        # Check that srt is generated
        mock_generate_srt.assert_called_once()
