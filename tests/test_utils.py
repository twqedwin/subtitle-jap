import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock dependencies
sys.modules['customtkinter'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['engine'] = MagicMock()
sys.modules['torch'] = MagicMock()

# Since gui/__init__.py imports app, we need to make sure app imports don't fail
# We might need to mock more modules if app.py imports them.
# app.py imports: config, components, engine, subtitle.
sys.modules['config'] = MagicMock()
sys.modules['subtitle'] = MagicMock()
# components imports customtkinter, time, typing. time and typing are standard.

class TestFileUtils(unittest.TestCase):

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_open_file_explorer_windows(self, mock_popen, mock_system):
        # We need to create the file first or mock the import
        # Here assuming gui/utils.py will be created
        try:
            from gui.utils import open_file_explorer
        except ImportError:
            # If the file doesn't exist, we can't test it yet.
            # This block is just to allow the test to run and fail with ImportError if file missing
            # instead of crashing due to other import errors.
            raise

        mock_system.return_value = 'Windows'
        path = r"C:\path\to\file.txt"

        open_file_explorer(path)

        mock_popen.assert_called_once_with(['explorer', '/select,', path])

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_open_file_explorer_mac(self, mock_popen, mock_system):
        from gui.utils import open_file_explorer

        mock_system.return_value = 'Darwin'
        path = "/path/to/file.txt"

        open_file_explorer(path)

        mock_popen.assert_called_once_with(['open', '-R', path])

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_open_file_explorer_linux(self, mock_popen, mock_system):
        from gui.utils import open_file_explorer

        mock_system.return_value = 'Linux'
        path = "/path/to/file.txt"
        parent_dir = "/path/to"

        open_file_explorer(path)

        mock_popen.assert_called_once_with(['xdg-open', parent_dir])

if __name__ == '__main__':
    unittest.main()
