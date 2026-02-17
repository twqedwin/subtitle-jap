"""
Custom UI components for the subtitle generator
"""

import customtkinter as ctk
from typing import Callable, Optional
import time


class ProgressPanel(ctk.CTkFrame):
    """
    Panel displaying progress bar and ETA information.
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.start_time = None
        self.last_progress = 0.0
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready to process",
            font=("SF Pro", 14),
            text_color=("gray30", "gray70")
        )
        self.status_label.pack(pady=(10, 5))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=400,
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(pady=10, padx=20)
        self.progress_bar.set(0)
        
        # Progress percentage label
        self.percentage_label = ctk.CTkLabel(
            self,
            text="0%",
            font=("SF Pro", 16, "bold"),
            text_color=("gray20", "gray80")
        )
        self.percentage_label.pack(pady=5)
        
        # ETA label
        self.eta_label = ctk.CTkLabel(
            self,
            text="",
            font=("SF Pro", 12),
            text_color=("gray40", "gray60")
        )
        self.eta_label.pack(pady=(5, 10))
    
    def update_progress(self, progress: float, status: str = "") -> None:
        """
        Update progress bar and status.
        
        Args:
            progress: Float between 0.0 and 1.0
            status: Optional status message
        """
        # Clamp progress
        progress = max(0.0, min(1.0, progress))
        
        # Update progress bar
        self.progress_bar.set(progress)
        
        # Update percentage
        percentage = int(progress * 100)
        self.percentage_label.configure(text=f"{percentage}%")
        
        # Update status message
        if status:
            self.status_label.configure(text=status)
        
        # Calculate and update ETA
        if self.start_time is None and progress > 0:
            self.start_time = time.time()
        
        if self.start_time and progress > 0.05:  # Only show ETA after 5% progress
            elapsed = time.time() - self.start_time
            total_estimated = elapsed / progress
            remaining = total_estimated - elapsed
            
            if remaining > 0:
                eta_text = self._format_time(remaining)
                self.eta_label.configure(text=f"Estimated time remaining: {eta_text}")
        
        self.last_progress = progress
        self.update_idletasks()
    
    def reset(self) -> None:
        """
        Reset progress panel to initial state.
        """
        self.start_time = None
        self.last_progress = 0.0
        self.progress_bar.set(0)
        self.percentage_label.configure(text="0%")
        self.status_label.configure(text="Ready to process")
        self.eta_label.configure(text="")
    
    def complete(self, success: bool = True, message: str = "") -> None:
        """
        Mark process as complete.
        
        Args:
            success: Whether process completed successfully
            message: Completion message
        """
        self.progress_bar.set(1.0)
        self.percentage_label.configure(text="100%")
        
        if message:
            self.status_label.configure(text=message)
        elif success:
            self.status_label.configure(text="✓ Complete!")
        else:
            self.status_label.configure(text="✗ Failed")
        
        self.eta_label.configure(text="")
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Format seconds into human-readable time string.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted string (e.g., "2m 30s")
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            mins = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{mins}m {secs}s"
        else:
            hours = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            return f"{hours}h {mins}m"


class DropZone(ctk.CTkFrame):
    """
    Drag-and-drop zone for video files.
    """
    
    def __init__(self, parent, on_file_selected: Callable[[str], None], **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_file_selected = on_file_selected
        self.selected_file = None
        
        # Configure appearance
        self.configure(
            fg_color=("gray85", "gray20"),
            border_color=("gray70", "gray30"),
            border_width=2,
            corner_radius=15
        )
        
        # Icon/instruction label
        self.label = ctk.CTkLabel(
            self,
            text="🎬\n\nDrag & Drop video file here\n(.mkv or .mp4)\nor click Browse",
            font=("SF Pro", 16),
            text_color=("gray50", "gray60")
        )
        self.label.pack(expand=True, pady=40)
        
        # Browse button
        self.browse_btn = ctk.CTkButton(
            self,
            text="Browse Files",
            command=self._browse_file,
            width=200,
            height=40,
            corner_radius=10,
            font=("SF Pro", 14)
        )
        self.browse_btn.pack(pady=(0, 30))
        
        # File info label (hidden initially)
        self.file_label = ctk.CTkLabel(
            self,
            text="",
            font=("SF Pro", 12),
            text_color=("gray40", "gray70")
        )
        
        # Enable drag and drop (macOS)
        self._setup_drag_drop()
    
    def _setup_drag_drop(self) -> None:
        """
        Set up drag and drop functionality for macOS.
        """
        # Note: tkinterdnd2 is needed for full drag-drop on macOS
        # For now, we'll rely on the browse button
        # TODO: Add tkinterdnd2 support if needed
        pass
    
    def _browse_file(self) -> None:
        """
        Open file browser to select video file.
        """
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video Files", "*.mkv *.mp4"),
                ("MKV Files", "*.mkv"),
                ("MP4 Files", "*.mp4"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self._on_file_dropped(file_path)
    
    def _on_file_dropped(self, file_path: str) -> None:
        """
        Handle file selection/drop.
        
        Args:
            file_path: Path to selected file
        """
        self.selected_file = file_path
        
        # Update UI to show selected file
        from pathlib import Path
        file_name = Path(file_path).name
        
        self.label.configure(text=f"✓ Selected:\n{file_name}")
        self.file_label.configure(text=f"📁 {file_path}")
        self.file_label.pack(pady=(0, 10))
        
        # Notify callback
        if self.on_file_selected:
            self.on_file_selected(file_path)
    
    def reset(self) -> None:
        """
        Reset drop zone to initial state.
        """
        self.selected_file = None
        self.label.configure(text="🎬\n\nDrag & Drop video file here\n(.mkv or .mp4)\nor click Browse")
        self.file_label.pack_forget()
    
    def get_selected_file(self) -> Optional[str]:
        """
        Get the currently selected file path.
        
        Returns:
            File path or None
        """
        return self.selected_file
