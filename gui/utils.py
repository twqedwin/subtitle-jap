import subprocess
import platform
import os
from pathlib import Path

def open_file_explorer(path: str) -> None:
    """
    Open the system file explorer and select the specified file.

    Args:
        path: Path to the file or directory to open
    """
    system = platform.system()
    path_obj = Path(path).resolve()

    try:
        if system == "Windows":
            subprocess.Popen(['explorer', '/select,', str(path_obj)])
        elif system == "Darwin":
            subprocess.Popen(['open', '-R', str(path_obj)])
        else:
            # Linux
            parent_dir = str(path_obj.parent)
            subprocess.Popen(['xdg-open', parent_dir])
    except Exception as e:
        print(f"Failed to open file explorer: {e}")
