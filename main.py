#!/usr/bin/env python3
"""
Japanese Subtitle Generator
High-performance subtitle generation for Japanese video files.
"""

import os
import sys
from pathlib import Path

# Fix for OpenMP library conflict on macOS
# This prevents "OMP: Error #15" when using PyTorch/numpy together
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from gui import SubtitleGeneratorApp


def main():
    """
    Main entry point for the application.
    """
    print("=" * 60)
    print("Japanese Subtitle Generator")
    print("Powered by faster-whisper + kotoba-whisper-v2.0-faster")
    print("=" * 60)
    print()
    
    # Run GUI application
    app = SubtitleGeneratorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
