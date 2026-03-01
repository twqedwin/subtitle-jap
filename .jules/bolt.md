
## 2025-05-24 - Faster-Whisper Internal FFmpeg Processing
**Learning:** `faster-whisper` uses FFmpeg internally and can process video files directly. The previous architecture explicitly extracted audio to a temporary `.wav` file on disk, which added unnecessary disk I/O, extra dependencies (`wave` module), and processing time.
**Action:** When working with `faster-whisper`, pass video files directly to `.transcribe()` and rely on `info.duration` instead of using the `wave` module or writing temporary extraction files.
