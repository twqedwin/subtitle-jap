## 2024-06-25 - Native Video Transcribing Performance optimization
**Learning:** `faster-whisper` natively handles video files via its internal FFmpeg wrapper, which avoids explicit disk extraction overhead (e.g. creating temporary WAV files).
**Action:** Always verify if a library's internal capabilities can bypass explicit data preparation steps like intermediate file I/O to improve performance. Also, ensure cleanup of unused modules after an optimization.
