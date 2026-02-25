import unittest
from unittest.mock import MagicMock
import sys

# Mock modules before import
whisper_mock = MagicMock()
sys.modules["faster_whisper"] = whisper_mock

# Mock wave to detect if it's used
wave_mock = MagicMock()
sys.modules["wave"] = wave_mock

# Mock other dependencies
sys.modules["torch"] = MagicMock()
sys.modules["ctranslate2"] = MagicMock()
sys.modules["ffmpeg"] = MagicMock()

# Import the class under test
from engine.transcriber import JapaneseTranscriber
import config

class TestTranscriberUnit(unittest.TestCase):
    def setUp(self):
        # We need to make sure we don't accidentally load the real model
        # The constructor calls load_model() ONLY IF explicitly called or if used incorrectly
        # JapaneseTranscriber() doesn't call load_model().

        self.transcriber = JapaneseTranscriber()
        # Mock the model directly on the instance
        self.model_mock = MagicMock()
        self.transcriber.model = self.model_mock

        # Reset mocks
        wave_mock.reset_mock()
        self.model_mock.reset_mock()

    def test_transcribe_uses_info_duration(self):
        """
        Verify that transcribe uses info.duration and does not use wave module.
        """
        audio_path = "test_video.mp4"

        # Setup model.transcribe return values
        mock_segments = iter([])  # Empty generator
        mock_info = MagicMock()
        mock_info.duration = 120.5
        mock_info.language = "ja"

        self.model_mock.transcribe.return_value = (mock_segments, mock_info)

        # Need to properly mock wave context manager for the current implementation
        # otherwise the test will error out instead of failing the assertion
        mock_wf = MagicMock()
        mock_wf.getnframes.return_value = 100
        mock_wf.getframerate.return_value = 1

        # Mock wave.open to return a context manager
        context_mock = MagicMock()
        context_mock.__enter__.return_value = mock_wf
        wave_mock.open.return_value = context_mock

        # Call transcribe
        self.transcriber.transcribe(audio_path)

        # Verification 1: wave should NOT be used
        # In current implementation, wave.open is called.
        # So this assertion should FAIL.
        wave_mock.open.assert_not_called()

        # Verification 2: transcribe should be called with audio_path
        # Use call_args to check arguments
        self.model_mock.transcribe.assert_called_once()
        args, kwargs = self.model_mock.transcribe.call_args
        self.assertEqual(args[0], audio_path)

if __name__ == "__main__":
    unittest.main()
