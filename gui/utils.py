import os
import platform
import subprocess
from pathlib import Path

def open_file_location(path: str) -> None:
    """
    Open the file location in the system's default file manager without blocking.

    Args:
        path: Path to the file or directory to reveal.
    """
    if not path:
        return

    p = Path(path)
    if not p.exists():
        return

    system = platform.system()

    try:
        if system == "Windows":
            # On Windows, /select, highlights the file
            subprocess.Popen(['explorer', '/select,', str(p)])
        elif system == "Darwin":
            # On macOS, -R reveals the file in Finder
            subprocess.Popen(['open', '-R', str(p)])
        else:
            # On Linux, typically we open the parent directory
            parent_dir = str(p.parent) if p.is_file() else str(p)
            subprocess.Popen(['xdg-open', parent_dir])
    except Exception as e:
        print(f"Failed to open location: {e}")
