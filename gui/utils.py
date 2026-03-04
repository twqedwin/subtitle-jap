import subprocess
import sys
from pathlib import Path

def open_file_explorer(path: str) -> None:
    """Open file explorer and select the given file if possible."""
    path_obj = Path(path)
    if not path_obj.exists():
        return

    try:
        if sys.platform == "win32":
            subprocess.Popen(['explorer', '/select,', str(path_obj)])
        elif sys.platform == "darwin":
            subprocess.Popen(['open', '-R', str(path_obj)])
        else:  # linux
            parent_dir = str(path_obj.parent)
            subprocess.Popen(['xdg-open', parent_dir])
    except Exception as e:
        print(f"Failed to open file explorer: {e}")
