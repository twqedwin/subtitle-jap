"""
Main GUI application for Japanese Subtitle Generator
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
from pathlib import Path
from typing import Optional

import config
from .components import ProgressPanel, DropZone
from engine import JapaneseTranscriber, extract_audio, cleanup_temp_audio
from subtitle import generate_srt, get_output_path


class SubtitleGeneratorApp(ctk.CTk):
    """
    Main application window for Japanese subtitle generation.
    """
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title(config.WINDOW_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode(config.THEME)
        ctk.set_default_color_theme("blue")
        
        # State
        self.processing = False
        self.current_file = None
        self.transcriber = None
        
        # Build UI
        self._build_ui()
        
        # Initialize transcriber (will load model on first use)
        self.transcriber = JapaneseTranscriber(
            progress_callback=self._on_transcription_progress
        )
    
    def _build_ui(self) -> None:
        """
        Build the user interface.
        """
        # Title
        title = ctk.CTkLabel(
            self,
            text="Japanese Subtitle Generator",
            font=("SF Pro Display", 28, "bold"),
            text_color=("gray10", "gray90")
        )
        title.pack(pady=(30, 10))
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            self,
            text="Powered by faster-whisper + kotoba-whisper-v2.0",
            font=("SF Pro", 12),
            text_color=("gray50", "gray60")
        )
        subtitle.pack(pady=(0, 20))
        
        # Drop zone
        self.drop_zone = DropZone(
            self,
            on_file_selected=self._on_file_selected,
            width=700,
            height=200
        )
        self.drop_zone.pack(pady=20, padx=50)
        
        # Progress panel
        self.progress_panel = ProgressPanel(self, width=700)
        self.progress_panel.pack(pady=20, padx=50)
        
        # Control buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="Generate Subtitles",
            command=self._start_processing,
            width=200,
            height=45,
            corner_radius=10,
            font=("SF Pro", 16, "bold"),
            state="disabled"
        )
        self.start_btn.pack(side="left", padx=10)
        
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._cancel_processing,
            width=120,
            height=45,
            corner_radius=10,
            font=("SF Pro", 16),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            state="disabled"
        )
        self.cancel_btn.pack(side="left", padx=10)
        
        # Hardware info
        from engine import detect_hardware
        hw_info = detect_hardware()
        device_text = f"Device: {hw_info['device_name']} ({hw_info['compute_type']})"
        
        device_label = ctk.CTkLabel(
            self,
            text=device_text,
            font=("SF Pro", 11),
            text_color=("gray50", "gray60")
        )
        device_label.pack(pady=(10, 20))
    
    def _on_file_selected(self, file_path: str) -> None:
        """
        Callback when file is selected.
        
        Args:
            file_path: Path to selected file
        """
        self.current_file = file_path
        self.start_btn.configure(state="normal")
    
    def _start_processing(self) -> None:
        """
        Start subtitle generation process.
        """
        if not self.current_file:
            messagebox.showerror("Error", "Please select a video file first")
            return
        
        # Disable controls
        self.processing = True
        self.start_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.drop_zone.browse_btn.configure(state="disabled")
        
        # Reset progress
        self.progress_panel.reset()
        
        # Start processing in background thread
        thread = threading.Thread(target=self._process_video, daemon=True)
        thread.start()
    
    def _process_video(self) -> None:
        """
        Process video file (runs in background thread).
        """
        audio_file = None
        
        try:
            # Step 1: Extract audio
            self._update_progress(0.0, "Extracting audio from video...")
            audio_file = extract_audio(self.current_file)
            
            # Step 2: Transcribe
            self._update_progress(0.2, "Loading model and starting transcription...")
            segments = self.transcriber.transcribe(audio_file)
            
            # Step 3: Generate SRT
            self._update_progress(0.9, "Generating subtitle file...")
            output_path = get_output_path(self.current_file)
            generate_srt(segments, output_path)
            
            # Complete
            self.after(0, lambda: self.progress_panel.complete(
                success=True,
                message=f"✓ Subtitles saved to: {Path(output_path).name}",
                output_path=output_path
            ))
            
        except Exception as e:
            error_msg = str(e)
            self._update_progress(0.0, f"✗ Error: {error_msg}")
            self.after(0, lambda: messagebox.showerror("Error", error_msg))
            
        finally:
            # Cleanup
            if audio_file:
                cleanup_temp_audio(audio_file)
            
            # Re-enable controls
            self.after(0, self._finish_processing)
    
    def _cancel_processing(self) -> None:
        """
        Cancel current processing.
        """
        # Note: Proper cancellation would require threading.Event
        # For now, just reset the UI
        self._finish_processing()
    
    def _finish_processing(self) -> None:
        """
        Finish processing and reset UI state.
        """
        self.processing = False
        self.start_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.drop_zone.browse_btn.configure(state="normal")
    
    def _on_transcription_progress(self, progress: float, message: str) -> None:
        """
        Callback for transcription progress updates.
        
        Args:
            progress: Progress value 0.0-1.0
            message: Status message
        """
        self._update_progress(progress, message)
    
    def _update_progress(self, progress: float, message: str) -> None:
        """
        Update progress display (thread-safe).
        
        Args:
            progress: Progress value 0.0-1.0
            message: Status message
        """
        self.after(0, lambda: self.progress_panel.update_progress(progress, message))


def run_app():
    """
    Run the application.
    """
    app = SubtitleGeneratorApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()
