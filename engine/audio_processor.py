"""
Audio extraction from video files using ffmpeg
"""

import os
import tempfile
import ffmpeg
from pathlib import Path
from typing import Optional


def extract_audio(video_path: str, output_path: Optional[str] = None) -> str:
    """
    Extract audio from video file without re-encoding.
    
    Args:
        video_path: Path to input video file (.mkv)
        output_path: Optional output path. If None, creates temp file.
    
    Returns:
        Path to extracted audio file
    
    Raises:
        FileNotFoundError: If video file doesn't exist
        RuntimeError: If ffmpeg extraction fails
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Create output path if not provided
    if output_path is None:
        # Create temporary WAV file
        temp_fd, output_path = tempfile.mkstemp(suffix=".wav", prefix="audio_")
        os.close(temp_fd)  # Close file descriptor, we just need the path
    
    try:
        print(f"Extracting audio from: {Path(video_path).name}")
        print(f"Output: {output_path}")
        
        # Extract audio using ffmpeg without re-encoding when possible
        # Convert to WAV for compatibility with faster-whisper
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(
            stream,
            output_path,
            acodec='pcm_s16le',  # 16-bit PCM (standard WAV format)
            ac=1,  # Mono audio (reduces processing time)
            ar='16000',  # 16kHz sample rate (optimal for Whisper)
            loglevel='error'  # Only show errors
        )
        
        # Overwrite output file if it exists
        stream = ffmpeg.overwrite_output(stream)
        
        # Run extraction
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
        
        print(f"✓ Audio extracted successfully")
        return output_path
        
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        raise RuntimeError(f"FFmpeg extraction failed: {error_message}")


def cleanup_temp_audio(audio_path: str) -> None:
    """
    Remove temporary audio file.
    
    Args:
        audio_path: Path to audio file to remove
    """
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"✓ Cleaned up temporary audio file")
    except Exception as e:
        print(f"⚠ Warning: Could not remove temp file {audio_path}: {e}")


if __name__ == "__main__":
    # Test audio extraction
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python audio_processor.py <video_file>")
        sys.exit(1)
    
    video_file = sys.argv[1]
    audio_file = extract_audio(video_file)
    print(f"Audio extracted to: {audio_file}")
    
    # Clean up
    input("Press Enter to cleanup temp file...")
    cleanup_temp_audio(audio_file)
