import subprocess
import os
import platform
from pathlib import Path

def open_file_explorer(path: str) -> None:
    """
    Open the file explorer and select the given file path.
    Cross-platform support for Windows, macOS, and Linux.
    """
    path = str(Path(path).resolve())

    if platform.system() == "Windows":
        subprocess.Popen(['explorer', '/select,', path])
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(['open', '-R', path])
    else:  # Linux and other UNIX-like OS
        # xdg-open doesn't support selecting a file, so we open its parent directory
        parent_dir = str(Path(path).parent)
        subprocess.Popen(['xdg-open', parent_dir])
