# Quick Start Guide

## Installation (One-Time Setup)

### Step 1: Run Setup Script
```bash
cd "/Volumes/Thumbdrive/subtitle generator"
./setup.sh
```

This will:
- Check Python and FFmpeg
- Create virtual environment
- Install all dependencies (~5-10 minutes)

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

---

## Usage

### Generate Subtitles (GUI)

```bash
python3 main.py
```

Then:
1. **Select File**: Click "Browse Files" or drag-and-drop a .mkv or .mp4 file
2. **Generate**: Click "Generate Subtitles"
3. **Wait**: Monitor progress bar and ETA
4. **Done**: Subtitle file (.srt) will be saved next to your video

### Example
```
Input:  /Movies/japanese_movie.mkv (or .mp4)
Output: /Movies/japanese_movie.srt
```

---

## Performance Expectations

| Hardware | 30-min Video | 2-hour Movie |
|----------|--------------|--------------|
| **NVIDIA GPU** | 3-5 min | 10-15 min |
| **CPU** | 10-15 min | 30-45 min |

---

## Troubleshooting

### "Module not found" error
```bash
# Make sure virtual environment is activated
source venv/bin/activate
```

### First run is slow
- Model is downloading (~1-3GB)
- Subsequent runs will be faster

### GPU not detected
- Check: `nvidia-smi`
- App will automatically use CPU fallback

---

## Deactivate Virtual Environment

When done:
```bash
deactivate
```

---

## Full Documentation

See [README.md](README.md) for detailed documentation.
