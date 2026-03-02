import unittest
from unittest.mock import MagicMock, patch

from engine.transcriber import JapaneseTranscriber
import config

class TestJapaneseTranscriber(unittest.TestCase):
    @patch('engine.transcriber.get_device_config')
    @patch('engine.transcriber.WhisperModel')
    def test_transcribe_video_file(self, MockWhisperModel, mock_get_device_config):
        # Setup mocks
        mock_get_device_config.return_value = ("cpu", "int8")

        mock_model_instance = MagicMock()
        MockWhisperModel.return_value = mock_model_instance

        # Mock segments_generator and info
        mock_segment1 = MagicMock()
        mock_segment1.start = 0.0
        mock_segment1.end = 2.0
        mock_segment1.text = " こんにちは "

        mock_segment2 = MagicMock()
        mock_segment2.start = 2.0
        mock_segment2.end = 4.0
        mock_segment2.text = " 本日は日本の映画を視聴しています "

        mock_segments_generator = [mock_segment1, mock_segment2]

        mock_info = MagicMock()
        mock_info.duration = 4.0 # Match info.duration used in refactored code

        mock_model_instance.transcribe.return_value = (mock_segments_generator, mock_info)

        # Initialize transcriber
        transcriber = JapaneseTranscriber()
        transcriber.load_model()

        # Execute
        video_path = "test_video.mkv"
        segments = transcriber.transcribe(video_path)

        # Assertions
        mock_model_instance.transcribe.assert_called_once_with(
            video_path,
            language=config.LANGUAGE,
            beam_size=config.BEAM_SIZE,
            temperature=config.TEMPERATURE,
            initial_prompt=config.INITIAL_PROMPT,
            vad_filter=config.VAD_FILTER,
            vad_parameters=config.VAD_PARAMETERS if config.VAD_FILTER else None,
            word_timestamps=False,
        )

        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0]['start'], 0.0)
        self.assertEqual(segments[0]['end'], 2.0)
        self.assertEqual(segments[0]['text'], "こんにちは")

        self.assertEqual(segments[1]['start'], 2.0)
        self.assertEqual(segments[1]['end'], 4.0)
        self.assertEqual(segments[1]['text'], "本日は日本の映画を視聴しています")

if __name__ == '__main__':
    unittest.main()
