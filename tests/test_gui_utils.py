import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import importlib.util
import types

# Create a dummy gui package to allow "from gui import utils" or "import gui.utils" to work
# if mechanisms try to look it up.
if 'gui' not in sys.modules:
    gui_pkg = types.ModuleType('gui')
    gui_pkg.__path__ = []
    sys.modules['gui'] = gui_pkg

# Load gui/utils.py directly
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../gui/utils.py'))
spec = importlib.util.spec_from_file_location("gui.utils", file_path)
utils_module = importlib.util.module_from_spec(spec)
sys.modules["gui.utils"] = utils_module
spec.loader.exec_module(utils_module)

open_file_in_explorer = utils_module.open_file_in_explorer

class TestGuiUtils(unittest.TestCase):

    def test_open_file_in_explorer_windows(self):
        with patch('gui.utils.os.path.exists') as mock_exists, \
             patch('gui.utils.subprocess.Popen') as mock_popen, \
             patch('gui.utils.platform.system') as mock_system:

            mock_exists.return_value = True
            mock_system.return_value = "Windows"

            test_path = "C:\\path\\to\\file.txt"
            open_file_in_explorer(test_path)

            mock_popen.assert_called_with(["explorer", "/select,", test_path])

    def test_open_file_in_explorer_macos(self):
        with patch('gui.utils.os.path.exists') as mock_exists, \
             patch('gui.utils.subprocess.Popen') as mock_popen, \
             patch('gui.utils.platform.system') as mock_system:

            mock_exists.return_value = True
            mock_system.return_value = "Darwin"

            test_path = "/path/to/file.txt"
            open_file_in_explorer(test_path)

            mock_popen.assert_called_with(["open", "-R", test_path])

    def test_open_file_in_explorer_linux(self):
        with patch('gui.utils.os.path.exists') as mock_exists, \
             patch('gui.utils.subprocess.Popen') as mock_popen, \
             patch('gui.utils.platform.system') as mock_system:

            mock_exists.return_value = True
            mock_system.return_value = "Linux"

            test_path = "/path/to/file.txt"

            open_file_in_explorer(test_path)

            parent_dir = os.path.dirname(test_path)
            mock_popen.assert_called_with(["xdg-open", parent_dir])

    def test_open_file_not_exists(self):
        with patch('gui.utils.os.path.exists') as mock_exists, \
             patch('gui.utils.subprocess.Popen') as mock_popen:

            mock_exists.return_value = False

            open_file_in_explorer("non_existent_file.txt")

            mock_popen.assert_not_called()

if __name__ == '__main__':
    unittest.main()
