## 2024-05-24 - Faster-Whisper Internal FFmpeg Processing
**Learning:** `faster-whisper` accepts video files directly for transcription via its internal FFmpeg integration. Explicit audio extraction to disk before transcription adds unnecessary disk I/O and processing time.
**Action:** Always pass video files directly to `faster-whisper` and use `info.duration` from the transcription result instead of the `wave` module or intermediate temporary files. Ensure orphaned code like `audio_processor.py` is fully removed.
