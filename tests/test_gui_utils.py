import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock customtkinter before importing gui.utils
sys.modules['customtkinter'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['engine'] = MagicMock()

# Now we can safely import gui.utils
# Note: gui.utils doesn't depend on ctk, but if the import chain triggers app.py, it might.
# However, if we import from gui.utils directly, it should be fine unless __init__.py is triggered.
# gui/__init__.py imports SubtitleGeneratorApp from .app
# gui/app.py imports customtkinter
# So simply importing gui.utils might trigger gui/__init__.py if not careful, or if we import from 'gui' package.
# Let's try to import directly from the file to avoid package init issues if possible,
# but python imports usually run __init__.py of the package.
# So mocking ctk is the right way.

from gui.utils import open_file_explorer

class TestGuiUtils(unittest.TestCase):

    def test_open_file_explorer_windows(self):
        with patch('gui.utils.platform.system', return_value='Windows'), \
             patch('gui.utils.subprocess.Popen') as mock_popen:

            test_path = r'C:\Users\test\file.txt'
            open_file_explorer(test_path)
            # Normalization might change slashes depending on the OS running the test
            # On Linux, r'C:\Users\test\file.txt' is treated as a relative path with backslashes in the name potentially?
            # actually os.path.normpath on linux won't change backslashes to forward slashes.
            # But let's check what logic we want.
            # If we are testing logic, we just want to ensure the call is passed through.

            mock_popen.assert_called_with(['explorer', '/select,', test_path])

    def test_open_file_explorer_macos(self):
        with patch('gui.utils.platform.system', return_value='Darwin'), \
             patch('gui.utils.subprocess.Popen') as mock_popen:

            test_path = '/Users/test/file.txt'
            open_file_explorer(test_path)

            mock_popen.assert_called_with(['open', '-R', test_path])

    def test_open_file_explorer_linux(self):
        with patch('gui.utils.platform.system', return_value='Linux'), \
             patch('gui.utils.subprocess.Popen') as mock_popen:

            test_path = '/home/test/file.txt'
            parent_dir = '/home/test'

            open_file_explorer(test_path)

            mock_popen.assert_called_with(['xdg-open', parent_dir])

if __name__ == '__main__':
    unittest.main()
