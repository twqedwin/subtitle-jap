## 2024-05-23 - [Optimization: Skip Audio Extraction]
**Learning:** `faster-whisper` can process video files directly via its internal FFmpeg/AV integration. We were redundantly extracting audio to a temporary WAV file using an external FFmpeg process, incurring disk I/O and process overhead.
**Action:** Always check if the consumption library supports the raw input format before creating intermediate processing steps. Pass video files directly to the transcriber.
