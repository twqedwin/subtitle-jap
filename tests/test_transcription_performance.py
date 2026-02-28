import sys
import unittest
from unittest.mock import MagicMock, patch

# Need to mock the heavy UI dependencies as mentioned in the memory
class MockCTk:
    def __init__(self, *args, **kwargs):
        pass
    def title(self, *args): pass
    def geometry(self, *args): pass
    def resizable(self, *args): pass

mock_ctk = MagicMock()
mock_ctk.CTk = MockCTk
sys.modules['customtkinter'] = mock_ctk
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()

# Instead of full gui imports which fail, let's just test that
# the _process_video logic works without calling extract_audio.
# Let's mock engine and subtitle before importing gui.app
sys.modules['engine'] = MagicMock()
sys.modules['subtitle'] = MagicMock()

from gui.app import SubtitleGeneratorApp

class TestTranscriptionPerformance(unittest.TestCase):
    def test_process_video_skips_extraction(self):
        """
        Verify that _process_video passes the file directly to transcribe
        and does not use extract_audio.
        """
        # Patch methods on app that we don't want to actually run
        with patch.object(SubtitleGeneratorApp, '_build_ui'), \
             patch.object(SubtitleGeneratorApp, '_update_progress'), \
             patch('gui.app.get_output_path', return_value='test.srt'), \
             patch('gui.app.generate_srt'):

            app = SubtitleGeneratorApp()
            app.current_file = "test_movie.mkv"
            app.transcriber = MagicMock()

            # Mock the lambda after
            app.after = MagicMock()

            # Run process video directly instead of via thread
            app._process_video()

            # Verify that transcribe was called with the video file path directly
            app.transcriber.transcribe.assert_called_once_with("test_movie.mkv")

if __name__ == '__main__':
    unittest.main()
