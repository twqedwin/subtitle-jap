"""
Utility functions for GUI
"""

import platform
import subprocess
from pathlib import Path

def open_file_explorer(path: str) -> None:
    """
    Open the file explorer and select the given file.
    """
    path_obj = Path(path)
    if platform.system() == "Windows":
        subprocess.Popen(['explorer', '/select,', str(path_obj)])
    elif platform.system() == "Darwin":
        subprocess.Popen(['open', '-R', str(path_obj)])
    else:
        # Linux
        subprocess.Popen(['xdg-open', str(path_obj.parent)])
