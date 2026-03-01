import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import os
import sys

# Mock imports for GUI module testing since we don't have dependencies installed
sys.modules['customtkinter'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['engine'] = MagicMock()
sys.modules['subtitle'] = MagicMock()

# Now we can import the utils module specifically, bypassing init
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import importlib.util
spec = importlib.util.spec_from_file_location("utils", "gui/utils.py")
utils = importlib.util.module_from_spec(spec)
sys.modules["utils"] = utils
spec.loader.exec_module(utils)
open_file_explorer = utils.open_file_explorer


class TestUtils(unittest.TestCase):
    @patch('utils.subprocess.Popen')
    @patch('utils.platform.system')
    def test_open_file_explorer_windows(self, mock_system, mock_popen):
        mock_system.return_value = 'Windows'
        test_path = 'C:/test/file.txt'
        expected_path = str(Path(test_path).resolve())
        open_file_explorer(test_path)
        mock_popen.assert_called_once_with(['explorer', '/select,', expected_path])

    @patch('utils.subprocess.Popen')
    @patch('utils.platform.system')
    def test_open_file_explorer_darwin(self, mock_system, mock_popen):
        mock_system.return_value = 'Darwin'
        test_path = '/Users/test/file.txt'
        expected_path = str(Path(test_path).resolve())
        open_file_explorer(test_path)
        mock_popen.assert_called_once_with(['open', '-R', expected_path])

    @patch('utils.subprocess.Popen')
    @patch('utils.platform.system')
    def test_open_file_explorer_linux(self, mock_system, mock_popen):
        mock_system.return_value = 'Linux'
        test_path = '/home/test/file.txt'
        expected_path = str(Path(test_path).resolve().parent)
        open_file_explorer(test_path)
        mock_popen.assert_called_once_with(['xdg-open', expected_path])

if __name__ == '__main__':
    unittest.main()
