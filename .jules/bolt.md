## 2024-02-28 - Eliminating explicit audio extraction
**Learning:** `faster-whisper` internally uses FFmpeg to decode audio on the fly directly from video files, meaning extracting a temporary WAV file is redundant.
**Action:** Removed explicit audio extraction to skip disk I/O, leveraging `info.duration` from the transcription result instead of reading WAV frames.
