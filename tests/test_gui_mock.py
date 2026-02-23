import unittest
from unittest.mock import MagicMock, patch
import sys
import threading
from pathlib import Path

# --- Mocking Dependencies ---

# Create dummy classes for customtkinter
class MockCTk:
    def __init__(self, *args, **kwargs):
        self.pack = MagicMock()
        self.pack_forget = MagicMock()
        self.grid = MagicMock()
        self.configure = MagicMock()
        self.after = MagicMock()
        self.title = MagicMock()
        self.geometry = MagicMock()
        self.resizable = MagicMock()
        self.mainloop = MagicMock()
        self.update_idletasks = MagicMock()
        self.winfo_ismapped = MagicMock(return_value=False)

class MockCTkFrame(MockCTk): pass
class MockCTkButton(MockCTk): pass
class MockCTkLabel(MockCTk): pass
class MockCTkEntry(MockCTk): pass
class MockCTkProgressBar(MockCTk):
    def set(self, value): pass

# Mock customtkinter module
mock_ctk = MagicMock()
mock_ctk.CTk = MockCTk
mock_ctk.CTkFrame = MockCTkFrame
mock_ctk.CTkButton = MockCTkButton
mock_ctk.CTkLabel = MockCTkLabel
mock_ctk.CTkEntry = MockCTkEntry
mock_ctk.CTkProgressBar = MockCTkProgressBar
sys.modules["customtkinter"] = mock_ctk

# Mock tkinter.messagebox
mock_tkinter = MagicMock()
mock_messagebox = MagicMock()
mock_tkinter.messagebox = mock_messagebox
sys.modules["tkinter"] = mock_tkinter
sys.modules["tkinter.messagebox"] = mock_messagebox

# Mock engine module
mock_engine = MagicMock()
mock_engine.extract_audio = MagicMock(return_value="audio.wav")
mock_engine.cleanup_temp_audio = MagicMock()
mock_transcriber = MagicMock()
mock_transcriber.transcribe = MagicMock(return_value=[])
mock_engine.JapaneseTranscriber = MagicMock(return_value=mock_transcriber)
mock_engine.detect_hardware = MagicMock(return_value={"device_name": "Test Device", "compute_type": "int8"})
sys.modules["engine"] = mock_engine

# Mock subtitle module
mock_subtitle = MagicMock()
mock_subtitle.generate_srt = MagicMock()
mock_subtitle.get_output_path = MagicMock(return_value="output.srt")
sys.modules["subtitle"] = mock_subtitle

# Mock config
sys.modules["config"] = MagicMock()

# Now import the app
from gui.app import SubtitleGeneratorApp

class TestSubtitleGeneratorApp(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_messagebox.showinfo.reset_mock()

        # Instantiate app
        self.app = SubtitleGeneratorApp()
        self.app.current_file = "test_video.mp4"
        self.app.after = MagicMock()

    def test_process_video_success_ux(self):
        """
        Verify that on success:
        1. Blocking messagebox is NOT shown.
        2. Open Folder button is configured and shown.
        """
        # Execute _process_video directly
        self.app._process_video()

        # Simulate the callbacks scheduled with after()
        # We need to find the callback that shows success UI

        callbacks_executed = 0
        for call in self.app.after.call_args_list:
            args, kwargs = call
            # after(delay, callback)
            if len(args) >= 2:
                callback = args[1]
                # Execute it
                try:
                    callback()
                    callbacks_executed += 1
                except Exception as e:
                    print(f"Callback failed: {e}")

        print(f"\n[TEST] Executed {callbacks_executed} callbacks.")

        # 1. Assert messagebox.showinfo was NOT called
        if mock_messagebox.showinfo.called:
            self.fail("messagebox.showinfo was called! It should be removed.")

        # 2. Assert open_folder_btn exists and was packed
        if not hasattr(self.app, 'open_folder_btn'):
            self.fail("open_folder_btn attribute not found on app instance.")

        self.app.open_folder_btn.pack.assert_called()
        print("[TEST] open_folder_btn.pack() was called.")

        # 3. Assert open_folder_btn command is set
        # We can't easily check the lambda, but we can check if configure was called
        self.app.open_folder_btn.configure.assert_called()

if __name__ == "__main__":
    unittest.main()
