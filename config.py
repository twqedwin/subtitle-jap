"""
Configuration settings for Japanese Subtitle Generator
"""

# Model Configuration
MODEL_NAME = "tiny"  # Smallest model for speed and stability
LANGUAGE = "ja"  # Japanese

# Transcription Parameters
BEAM_SIZE = 5
TEMPERATURE = 0.0  # More deterministic output
INITIAL_PROMPT = "こんにちは。本日は日本の映画を視聴しています。"

# Performance Settings
VAD_FILTER = False  # Disabled VAD to prevent segfault on some macOS systems
VAD_PARAMETERS = {
    "threshold": 0.5,
    "min_speech_duration_ms": 250,
    "min_silence_duration_ms": 100,
}

# Subtitle Formatting
MAX_LINE_LENGTH = 42  # Characters per line (Japanese)
MAX_LINES_PER_SUBTITLE = 2
MIN_SUBTITLE_DURATION = 1.0  # seconds
MAX_SUBTITLE_DURATION = 7.0  # seconds

# UI Settings
WINDOW_TITLE = "Japanese Subtitle Generator"
WINDOW_SIZE = "800x700"  # Increased height to fit all elements
THEME = "dark"

# File Settings
SUPPORTED_VIDEO_FORMATS = [".mkv", ".mp4"]
OUTPUT_SUBTITLE_FORMAT = ".srt"
TEMP_AUDIO_FORMAT = ".wav"
