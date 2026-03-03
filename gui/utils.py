import platform
import subprocess
from pathlib import Path


def open_file_explorer(path: str) -> None:
    """
    Open the file explorer to the given path in a non-blocking way.

    Args:
        path: The file or directory path to open/select.
    """
    path_obj = Path(path)
    system = platform.system()

    try:
        if system == "Windows":
            subprocess.Popen(["explorer", "/select,", str(path_obj)])
        elif system == "Darwin":
            subprocess.Popen(["open", "-R", str(path_obj)])
        else:
            # Linux usually expects the parent directory
            subprocess.Popen(["xdg-open", str(path_obj.parent)])
    except Exception as e:
        print(f"Failed to open file explorer: {e}")
