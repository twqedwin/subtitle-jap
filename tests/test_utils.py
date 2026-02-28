import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import platform
import sys
from pathlib import Path

# Mock modules before importing gui modules
sys.modules['customtkinter'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['engine'] = MagicMock()
sys.modules['subtitle'] = MagicMock()

from gui.utils import open_file_location

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to test with
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file_path = os.path.join(self.temp_dir.name, "test_file.txt")
        with open(self.temp_file_path, 'w') as f:
            f.write("test content")

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch('gui.utils.subprocess.Popen')
    def test_open_file_location_windows(self, mock_popen):
        with patch('gui.utils.platform.system', return_value='Windows'):
            open_file_location(self.temp_file_path)
            mock_popen.assert_called_once_with(['explorer', '/select,', self.temp_file_path])

    @patch('gui.utils.subprocess.Popen')
    def test_open_file_location_mac(self, mock_popen):
        with patch('gui.utils.platform.system', return_value='Darwin'):
            open_file_location(self.temp_file_path)
            mock_popen.assert_called_once_with(['open', '-R', self.temp_file_path])

    @patch('gui.utils.subprocess.Popen')
    def test_open_file_location_linux_file(self, mock_popen):
        with patch('gui.utils.platform.system', return_value='Linux'):
            open_file_location(self.temp_file_path)
            mock_popen.assert_called_once_with(['xdg-open', str(Path(self.temp_file_path).parent)])

    @patch('gui.utils.subprocess.Popen')
    def test_open_file_location_linux_dir(self, mock_popen):
        with patch('gui.utils.platform.system', return_value='Linux'):
            open_file_location(self.temp_dir.name)
            mock_popen.assert_called_once_with(['xdg-open', self.temp_dir.name])

    @patch('gui.utils.subprocess.Popen')
    def test_open_file_location_nonexistent(self, mock_popen):
        open_file_location("nonexistent_path_that_does_not_exist_123.txt")
        mock_popen.assert_not_called()

    @patch('gui.utils.subprocess.Popen')
    def test_open_file_location_empty(self, mock_popen):
        open_file_location("")
        mock_popen.assert_not_called()

    @patch('gui.utils.subprocess.Popen')
    def test_open_file_location_none(self, mock_popen):
        open_file_location(None)
        mock_popen.assert_not_called()

if __name__ == '__main__':
    unittest.main()
