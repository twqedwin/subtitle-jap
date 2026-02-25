"""
Utility functions for GUI application
"""

import platform
import subprocess
import os
from pathlib import Path

def open_file_in_explorer(path: str) -> None:
    """
    Open the file explorer and select the specified file.

    Args:
        path: Path to the file to show
    """
    if not path or not os.path.exists(path):
        return

    path = os.path.normpath(path)
    system = platform.system()

    try:
        if system == "Windows":
            subprocess.Popen(["explorer", "/select,", path])
        elif system == "Darwin":
            subprocess.Popen(["open", "-R", path])
        else:
            # Linux and others - open parent folder
            parent = os.path.dirname(path)
            subprocess.Popen(["xdg-open", parent])
    except Exception as e:
        print(f"Error opening file explorer: {e}")
