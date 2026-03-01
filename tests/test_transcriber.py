import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock modules that might not be installed in the test environment
sys.modules['torch'] = MagicMock()
sys.modules['faster_whisper'] = MagicMock()
sys.modules['ffmpeg'] = MagicMock()

from engine.transcriber import JapaneseTranscriber

class TestJapaneseTranscriber(unittest.TestCase):
    @patch('engine.transcriber.get_device_config')
    def test_transcribe_video_directly(self, mock_get_device):
        mock_get_device.return_value = ('cpu', 'int8')
        mock_model_instance = MagicMock()

        # Mock generator and info return
        mock_segment = MagicMock()
        mock_segment.start = 0.0
        mock_segment.end = 2.0
        mock_segment.text = "テスト"
        mock_generator = [mock_segment]

        mock_info = MagicMock()
        mock_info.duration = 5.0

        mock_model_instance.transcribe.return_value = (mock_generator, mock_info)

        transcriber = JapaneseTranscriber()
        transcriber.model = mock_model_instance # Inject directly
        segments = transcriber.transcribe('fake_video.mp4')

        # Verify directly passing the path to the model
        mock_model_instance.transcribe.assert_called_once()
        self.assertEqual(mock_model_instance.transcribe.call_args[0][0], 'fake_video.mp4')
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]['text'], "テスト")

if __name__ == '__main__':
    unittest.main()
