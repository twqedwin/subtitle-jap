import sys
from unittest.mock import MagicMock
import unittest

# Create a proper class for CTk so inheritance works correctly
class MockCTk:
    def __init__(self, *args, **kwargs):
        pass

    def after(self, delay, callback):
        # Invoke callback immediately
        callback()

    def title(self, *args): pass
    def geometry(self, *args): pass
    def resizable(self, *args): pass
    def pack(self, *args): pass
    def configure(self, *args, **kwargs): pass
    def mainloop(self): pass

# Mock customtkinter before importing gui.app
ctk_mock = MagicMock()
ctk_mock.CTk = MockCTk
ctk_mock.set_appearance_mode = MagicMock()
ctk_mock.set_default_color_theme = MagicMock()

sys.modules["customtkinter"] = ctk_mock
sys.modules["tkinter"] = MagicMock()
sys.modules["tkinter.messagebox"] = MagicMock()

# Mock engine module
engine_mock = MagicMock()
sys.modules["engine"] = engine_mock

# Configure engine mock
extract_audio_mock = MagicMock(return_value="temp.wav")
cleanup_temp_audio_mock = MagicMock()
transcriber_class_mock = MagicMock()
transcriber_instance_mock = MagicMock()
transcriber_class_mock.return_value = transcriber_instance_mock

engine_mock.extract_audio = extract_audio_mock
engine_mock.cleanup_temp_audio = cleanup_temp_audio_mock
engine_mock.JapaneseTranscriber = transcriber_class_mock

# Mock subtitle module
sys.modules["subtitle"] = MagicMock()

# Import the module under test
import gui.app

class TestGUI(unittest.TestCase):
    def setUp(self):
        # Create app instance with minimal setup
        self.app = gui.app.SubtitleGeneratorApp()
        self.app.current_file = "test_video.mp4"

        # Reset mocks before each test
        extract_audio_mock.reset_mock()
        transcriber_instance_mock.transcribe.reset_mock()
        cleanup_temp_audio_mock.reset_mock()

    def test_process_video_flow(self):
        """Test that video processing optimizes by skipping extraction"""
        self.app._process_video()

        # extract_audio should NOT be called
        extract_audio_mock.assert_not_called()

        # Transcribe should be called with the video file directly
        transcriber_instance_mock.transcribe.assert_called_once_with("test_video.mp4")

        # Cleanup should NOT be called (no temp file)
        cleanup_temp_audio_mock.assert_not_called()

if __name__ == "__main__":
    unittest.main()
