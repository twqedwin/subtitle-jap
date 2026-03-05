import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock dependencies before importing app
sys.modules['customtkinter'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['engine'] = MagicMock()
sys.modules['subtitle'] = MagicMock()

# Since ctk.CTk is inherited by SubtitleGeneratorApp, we need a functional mock class
class MockCTk:
    def __init__(self):
        self.after_calls = []
    def title(self, *args, **kwargs): pass
    def geometry(self, *args, **kwargs): pass
    def resizable(self, *args, **kwargs): pass
    def mainloop(self): pass
    def update_idletasks(self): pass
    def after(self, delay, callback):
        self.after_calls.append(callback)
        callback()
    def pack(self, *args, **kwargs): pass
    def pack_forget(self): pass

sys.modules['customtkinter'].CTk = MockCTk

# Now we can safely import app
import gui.app
# Mock DropZone and ProgressPanel so they don't break mock execution
gui.app.DropZone = MagicMock()
gui.app.ProgressPanel = MagicMock()

from gui.app import SubtitleGeneratorApp

class TestUIUXImprovements(unittest.TestCase):
    @patch('engine.JapaneseTranscriber')
    def setUp(self, MockTranscriber):
        # Setup mocks for UI elements
        self.app = SubtitleGeneratorApp()
        self.app.start_btn = MagicMock()
        self.app.cancel_btn = MagicMock()
        self.app.open_loc_btn = MagicMock()
        self.app.drop_zone = MagicMock()
        self.app.progress_panel = MagicMock()

    def test_start_processing_hides_open_loc_btn(self):
        self.app.current_file = "test.mkv"

        # Override threading to not start a background thread for this test
        with patch('threading.Thread'):
            self.app._start_processing()

            # Verify open_loc_btn was unpacked
            self.app.open_loc_btn.pack_forget.assert_called()

            # Verify main controls were repacked correctly
            self.app.start_btn.pack.assert_called_with(side="left", padx=10)
            self.app.cancel_btn.pack.assert_called_with(side="left", padx=10)

    def test_show_success_reveals_open_loc_btn(self):
        test_path = "/path/to/test.srt"
        self.app._show_success(test_path)

        # Verify sequence of repacking to maintain layout
        self.app.start_btn.pack_forget.assert_called()
        self.app.cancel_btn.pack_forget.assert_called()
        self.app.open_loc_btn.pack_forget.assert_called()

        self.app.start_btn.pack.assert_called_with(side="left", padx=10)
        self.app.cancel_btn.pack.assert_called_with(side="left", padx=10)
        self.app.open_loc_btn.pack.assert_called_with(side="left", padx=10)

        self.assertEqual(self.app.output_path, test_path)

    @patch('gui.app.open_file_explorer')
    def test_open_output_location(self, mock_open):
        test_path = "/path/to/test.srt"
        self.app.output_path = test_path
        self.app._open_output_location()

        mock_open.assert_called_once_with(test_path)

if __name__ == '__main__':
    unittest.main()
