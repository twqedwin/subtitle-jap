import platform
import subprocess
import os

def open_file_explorer(path):
    """
    Opens the file explorer and selects the file.

    Args:
        path: Path to the file or directory to open.
    """
    system_name = platform.system()
    path = os.path.normpath(path)

    if system_name == 'Windows':
        subprocess.Popen(['explorer', '/select,', path])
    elif system_name == 'Darwin':  # macOS
        subprocess.Popen(['open', '-R', path])
    elif system_name == 'Linux':
        # On Linux, selecting a specific file is not standardized across file managers.
        # We'll open the parent directory instead.
        parent_dir = os.path.dirname(path)
        subprocess.Popen(['xdg-open', parent_dir])
    else:
        # Fallback for other OSs, try to just open the file/dir
        try:
            os.startfile(path)
        except AttributeError:
            subprocess.Popen(['xdg-open', path])
