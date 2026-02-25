## 2024-05-22 - Optimizing faster-whisper Audio Processing
**Learning:** `faster-whisper` handles media decoding internally using FFmpeg/av, so explicit audio extraction to WAV is redundant and wastes I/O and disk space.
**Action:** Pass video files directly to `model.transcribe()` instead of extracting audio separately, and use `info.duration` from the result instead of `wave` module.
