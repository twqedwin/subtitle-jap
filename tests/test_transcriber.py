import unittest
from unittest.mock import patch, MagicMock

class TestTranscriber(unittest.TestCase):

    @patch('engine.transcriber.WhisperModel')
    @patch('engine.transcriber.get_device_config')
    def test_transcribe_uses_info_duration(self, mock_get_device_config, mock_whisper_model):
        mock_get_device_config.return_value = ('cpu', 'int8')
        mock_model_instance = MagicMock()
        mock_whisper_model.return_value = mock_model_instance

        mock_info = MagicMock()
        mock_info.duration = 100.0

        mock_segment = MagicMock()
        mock_segment.start = 0.0
        mock_segment.end = 10.0
        mock_segment.text = "Test segment"

        # transcribe returns a generator of segments and info
        mock_model_instance.transcribe.return_value = ([mock_segment], mock_info)

        from engine.transcriber import JapaneseTranscriber
        transcriber = JapaneseTranscriber()
        segments = transcriber.transcribe('dummy_video.mp4')

        # Verify faster-whisper transcribe was called with the video file
        mock_model_instance.transcribe.assert_called_once()
        self.assertEqual(mock_model_instance.transcribe.call_args[0][0], 'dummy_video.mp4')

        # Verify segment output
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]['text'], "Test segment")
