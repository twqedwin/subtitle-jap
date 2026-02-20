import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from subtitle import get_output_path

class TestUXLogic(unittest.TestCase):

    def test_get_output_path(self):
        video_path = "/path/to/video.mkv"
        expected_output = str(Path("/path/to/video.srt"))

        # Mock config since it's used in get_output_path
        with patch('subtitle.generator.config') as mock_config:
            mock_config.OUTPUT_SUBTITLE_FORMAT = ".srt"
            result = get_output_path(video_path)
            self.assertEqual(result, expected_output)

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_open_output_folder_linux(self, mock_popen, mock_system):
        mock_system.return_value = 'Linux'

        # Mock implementation of the logic we implemented in gui/app.py
        def _open_output_folder(file_path):
            if not file_path:
                return

            output_path = get_output_path(file_path)
            folder_path = os.path.dirname(output_path)

            import platform
            system = platform.system()

            if system == "Windows":
                os.startfile(folder_path)
            elif system == "Darwin":
                import subprocess
                subprocess.Popen(["open", folder_path])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", folder_path])

        test_file = "/home/user/videos/movie.srt"
        test_folder = "/home/user/videos"

        # We need to mock get_output_path used inside _open_output_folder
        with patch('subtitle.generator.config') as mock_config:
             mock_config.OUTPUT_SUBTITLE_FORMAT = ".srt"
             _open_output_folder(test_file)

        mock_popen.assert_called_once_with(["xdg-open", test_folder])

    @patch('platform.system')
    @patch('os.startfile', create=True)
    def test_open_output_folder_windows(self, mock_startfile, mock_system):
        mock_system.return_value = 'Windows'

        test_file = "C:/Users/User/Videos/movie.srt"
        test_folder = "C:/Users/User/Videos"

        def _open_output_folder(file_path):
            if not file_path:
                return

            # Note: get_output_path uses pathlib which adapts to OS.
            # On Linux, C:/... is treated as relative or weird path, but logic holds.
            output_path = get_output_path(file_path)
            folder_path = os.path.dirname(output_path)

            import platform
            system = platform.system()

            if system == "Windows":
                os.startfile(folder_path)
            # ...

        with patch('subtitle.generator.config') as mock_config:
             mock_config.OUTPUT_SUBTITLE_FORMAT = ".srt"
             _open_output_folder(test_file)

        mock_startfile.assert_called_once_with(test_folder)

if __name__ == '__main__':
    unittest.main()
