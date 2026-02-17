# Japanese Subtitle Generator

A high-performance desktop application for generating accurate Japanese subtitles from .mkv and .mp4 files using faster-whisper and the kotoba-whisper-v2.0-faster model.

## Features

✨ **High Accuracy**: Uses kotoba-whisper-v2.0-faster model specifically trained for Japanese
🚀 **Fast Processing**: Processes a 2-hour movie in under 15 minutes (GPU)  
🎮 **GPU Acceleration**: Automatic NVIDIA CUDA detection with CPU fallback
🎨 **Modern UI**: Drag-and-drop interface with real-time progress tracking
📊 **ETA Display**: Estimated time remaining for long videos
🇯🇵 **Japanese Optimized**: Smart line-breaking and formatting for Japanese text
🎬 **Multiple Formats**: Supports both .mkv and .mp4 video files

## System Requirements

### Required
- **Python**: 3.8 or higher
- **FFmpeg**: For audio extraction
- **Operating System**: macOS, Windows, or Linux

### Recommended
- **GPU**: NVIDIA GPU with CUDA support (for faster processing)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 3GB for model cache

## Installation

### 1. Install FFmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. Install Python Dependencies

```bash
cd "/Volumes/Thumbdrive/subtitle generator"
pip install -r requirements.txt
```

**Note for GPU Users:**
If you have an NVIDIA GPU and want CUDA acceleration, install PyTorch with CUDA:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. First Run Model Download

On first run, the kotoba-whisper-v2.0-faster model (~1-3GB) will be automatically downloaded. This may take a few minutes depending on your internet connection.

## Usage

### GUI Mode (Recommended)

1. Launch the application:
```bash
python3 main.py
```

2. **Select Video**: 
   - Drag and drop a .mkv or .mp4 file into the window, OR
   - Click "Browse Files" to select a file

3. **Generate Subtitles**: 
   - Click "Generate Subtitles"
   - Monitor progress with the real-time progress bar and ETA

4. **Output**: 
   - Subtitles will be saved as `.srt` in the same directory as your video
   - Example: `movie.mkv` → `movie.srt` or `movie.mp4` → `movie.srt`

### Command Line Testing

You can test individual components:

**Test hardware detection:**
```bash
python engine/hardware.py
```

**Test audio extraction:**
```bash
python engine/audio_processor.py your_video.mkv
```

**Test transcription:**
```bash
python engine/transcriber.py audio_file.wav
```

## Performance

### Expected Processing Times

**With NVIDIA GPU (CUDA):**
- 30-minute video: ~3-5 minutes
- 2-hour movie: ~10-15 minutes
- Real-time factor: ~0.1-0.15x

**With CPU (INT8):**
- 30-minute video: ~10-15 minutes
- 2-hour movie: ~30-45 minutes
- Real-time factor: ~0.3-0.4x

*Times vary based on hardware specs and audio complexity*

## Configuration

Edit `config.py` to customize:

```python
# Transcription quality
BEAM_SIZE = 5  # Higher = more accurate but slower (1-10)
TEMPERATURE = 0.0  # Lower = more deterministic

# Subtitle formatting
MAX_LINE_LENGTH = 42  # Characters per line
MAX_LINES_PER_SUBTITLE = 2

# UI theme
THEME = "dark"  # "dark" or "light"
```

## Troubleshooting

### Model Download Issues
If the model download fails:
1. Check your internet connection
2. Clear the cache: `rm -rf ~/.cache/huggingface/`
3. Retry: `python3 main.py`

### CUDA Not Detected
If you have an NVIDIA GPU but it's not detected:
1. Verify CUDA installation: `nvidia-smi`
2. Reinstall PyTorch with CUDA support (see installation steps)
3. Check GPU compatibility with CUDA 11.8+

### FFmpeg Not Found
If you get "ffmpeg not found" error:
1. Verify installation: `ffmpeg -version`
2. Make sure FFmpeg is in your system PATH
3. Restart terminal after installation

### Out of Memory (GPU)
If you get CUDA out of memory errors:
1. Close other GPU-intensive applications
2. The app will automatically fallback to CPU
3. Edit `config.py` and set `compute_type = "int8"` for GPU

### OpenMP Library Conflict (macOS)
If you see "OMP: Error #15: Initializing libiomp5.dylib":
- This is already fixed in the code (sets `KMP_DUPLICATE_LIB_OK=TRUE`)
- If it persists, run: `export KMP_DUPLICATE_LIB_OK=TRUE` before running the app
- This is a harmless conflict between PyTorch and numpy on macOS

### Segmentation Fault on CPU (macOS)
If the app crashes with a segmentation fault when loading the model:
- This has been fixed by using float32 instead of int8 for CPU
- The app will automatically use the compatible compute type
- Performance may be slightly slower but more stable

### Subtitle Timing Issues
If subtitles are not synced properly:
1. Check if the video has variable frame rate
2. Try re-encoding the audio stream
3. Report the issue with video specifications

## Technical Details

### Architecture
- **Transcription Engine**: faster-whisper (optimized Whisper implementation)
- **Model**: kotoba-whisper-v2.0-faster (Japanese-specific)
- **Audio Processing**: FFmpeg (no re-encoding, 16kHz mono WAV)
- **GUI Framework**: CustomTkinter (modern, cross-platform)
- **Subtitle Format**: SRT with UTF-8 encoding

### Japanese Optimization
- Beam search with size=5 for better accuracy
- Initial prompt for Kanji/Kana context
- Voice Activity Detection (VAD) for faster processing
- Smart line-breaking at Japanese punctuation
- Segment merging for better readability

## License

This project uses the following open-source components:
- faster-whisper (MIT License)
- kotoba-whisper-v2.0-faster (Apache 2.0)
- CustomTkinter (MIT License)
- FFmpeg (LGPL/GPL)

## Support

For issues, questions, or feature requests, please check:
1. This README's troubleshooting section
2. Configuration options in `config.py`
3. Component test scripts for debugging

---

**Enjoy accurate Japanese subtitles! 🎬🇯🇵**
