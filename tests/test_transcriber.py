import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Create dummy modules to allow import if dependencies are missing
sys.modules['faster_whisper'] = MagicMock()
sys.modules['customtkinter'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['torch'] = MagicMock()
sys.modules['ffmpeg'] = MagicMock()

# Mock wave globally
mock_wave = MagicMock()
sys.modules['wave'] = mock_wave

# Now import the module to test
from engine.transcriber import JapaneseTranscriber
import config

class TestTranscriber(unittest.TestCase):
    def setUp(self):
        pass

    def test_transcribe_does_not_use_wave(self):
        transcriber = JapaneseTranscriber()
        transcriber.model = MagicMock()

        # Reset mock_wave
        mock_wave.reset_mock()

        # Setup mock for model.transcribe
        # It returns (segments_generator, info)
        segment = MagicMock()
        segment.start = 0.0
        segment.end = 5.0
        segment.text = "Hello"

        info = MagicMock()
        info.duration = 10.0

        transcriber.model.transcribe.return_value = ([segment], info)

        # Call transcribe with a fake video file
        transcriber.transcribe("dummy_video.mkv")

        # Verify wave was NOT used
        mock_wave.open.assert_not_called()

        # Verify model.transcribe called with the file path
        # Check arguments passed to transcribe
        # audio_path is the first arg
        args, kwargs = transcriber.model.transcribe.call_args
        self.assertEqual(args[0], "dummy_video.mkv")

if __name__ == '__main__':
    unittest.main()
