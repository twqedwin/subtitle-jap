"""
Utility functions for the GUI application.
"""

import platform
import subprocess
import os
import sys

def open_file_explorer(path: str) -> None:
    """
    Open the file explorer and select the specified file.

    Args:
        path: Path to the file to show in explorer.
    """
    system = platform.system()
    try:
        if system == "Windows":
             subprocess.Popen(["explorer", "/select,", path])
        elif system == "Darwin":
             subprocess.Popen(["open", "-R", path])
        elif system == "Linux":
             parent_dir = os.path.dirname(path)
             subprocess.Popen(["xdg-open", parent_dir])
        else:
            print(f"Unsupported operating system: {system}")
    except Exception as e:
        print(f"Failed to open file explorer: {e}")
