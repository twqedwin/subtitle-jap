import unittest
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock external dependencies
sys.modules['customtkinter'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()

# Mock engine module (it has external deps like torch)
mock_engine = MagicMock()
sys.modules['engine'] = mock_engine
sys.modules['engine.transcriber'] = MagicMock()
sys.modules['engine.audio_processor'] = MagicMock()
sys.modules['engine.hardware'] = MagicMock()

# Setup attributes for engine imports
mock_engine.JapaneseTranscriber = MagicMock()
mock_engine.extract_audio = MagicMock()
mock_engine.cleanup_temp_audio = MagicMock()
mock_engine.detect_hardware = MagicMock()

class TestImports(unittest.TestCase):

    def test_gui_app_import(self):
        """
        Verify that gui.app can be imported without NameError or ImportError
        (except for mocked modules).
        """
        try:
            from gui.app import SubtitleGeneratorApp
            self.assertTrue(True, "Successfully imported SubtitleGeneratorApp")
        except ImportError as e:
            self.fail(f"ImportError during gui.app import: {e}")
        except NameError as e:
            self.fail(f"NameError during gui.app import: {e}")
        except Exception as e:
            self.fail(f"Unexpected error during gui.app import: {e}")

if __name__ == '__main__':
    unittest.main()
