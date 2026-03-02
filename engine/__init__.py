"""
Engine module for audio processing and transcription
"""

from .hardware import detect_hardware, get_device_config
# ⚡ Bolt: Removed extract_audio and cleanup_temp_audio from exports
# since explicit extraction is skipped to improve disk I/O.
# audio_processor.py remains available as a dev utility.
from .transcriber import JapaneseTranscriber

__all__ = [
    "detect_hardware",
    "get_device_config",
    "JapaneseTranscriber",
]
