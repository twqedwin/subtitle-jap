import sys
import unittest
from unittest.mock import MagicMock, patch

# Define Mock Classes
class MockCTk:
    def __init__(self, *args, **kwargs):
        self.tk = MagicMock()
        pass
    def title(self, *args): pass
    def geometry(self, *args): pass
    def resizable(self, *args): pass
    def after(self, *args, **kwargs): pass
    def mainloop(self): pass

class MockCTkButton:
    def __init__(self, *args, **kwargs):
        self.master = kwargs.get('master')
    def pack(self, *args, **kwargs): pass
    def pack_forget(self): pass
    def configure(self, *args, **kwargs): pass

class MockCTkLabel:
    def __init__(self, *args, **kwargs):
        pass
    def pack(self, *args, **kwargs): pass
    def configure(self, *args, **kwargs): pass

class MockCTkFrame:
    def __init__(self, *args, **kwargs):
        pass
    def pack(self, *args, **kwargs): pass

class MockProgressPanel:
    def __init__(self, *args, **kwargs):
        pass
    def pack(self, *args, **kwargs): pass
    def reset(self): pass
    def update_progress(self, *args): pass

class MockDropZone:
    def __init__(self, *args, **kwargs):
        self.browse_btn = MockCTkButton()
    def pack(self, *args, **kwargs): pass

# Mock modules
mock_ctk = MagicMock()
mock_ctk.CTk = MockCTk
mock_ctk.CTkButton = MockCTkButton
mock_ctk.CTkLabel = MockCTkLabel
mock_ctk.CTkFrame = MockCTkFrame
mock_ctk.set_appearance_mode = MagicMock()
mock_ctk.set_default_color_theme = MagicMock()

sys.modules["customtkinter"] = mock_ctk
sys.modules["tkinter"] = MagicMock()
sys.modules["tkinter.messagebox"] = MagicMock()
sys.modules["engine"] = MagicMock()
sys.modules["subtitle"] = MagicMock()

# Mock components inside gui.app import
# We can't easily mock `from .components import ...` without mocking sys.modules['gui.components']
sys.modules['gui.components'] = MagicMock()
sys.modules['gui.components'].ProgressPanel = MockProgressPanel
sys.modules['gui.components'].DropZone = MockDropZone

# Now import
try:
    from gui.app import SubtitleGeneratorApp
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

class TestSubtitleGeneratorAppStructure(unittest.TestCase):
    def setUp(self):
        try:
            self.app = SubtitleGeneratorApp()
        except Exception as e:
            self.fail(f"Failed to instantiate SubtitleGeneratorApp: {e}")

    def test_attributes_exist(self):
        self.assertIsNone(self.app.last_output_path)
        self.assertTrue(hasattr(self.app, "open_folder_btn"))
        self.assertTrue(hasattr(self.app, "_open_output_folder"))
        self.assertTrue(hasattr(self.app, "_show_success"))

    @patch("os.path.exists")
    def test_show_success_logic(self, mock_exists):
        mock_exists.return_value = True

        # We need to mock pack_forget and pack for the buttons if not already handled by MockCTkButton
        # Our MockCTkButton has these methods.

        # We also need to mock pack_forget on cancel_btn specifically to track calls
        self.app.cancel_btn.pack_forget = MagicMock()
        self.app.open_folder_btn.pack = MagicMock()

        output_path = "/tmp/test.srt"

        self.app._show_success(output_path)

        self.assertEqual(self.app.last_output_path, output_path)
        self.app.cancel_btn.pack_forget.assert_called_once()
        self.app.open_folder_btn.pack.assert_called_with(side="left", padx=10)

if __name__ == "__main__":
    unittest.main()
