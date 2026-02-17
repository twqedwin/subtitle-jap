"""
SRT subtitle file generation
"""

from typing import List
from pathlib import Path
import config
from .formatter import format_japanese_text, merge_short_segments


def format_timestamp(seconds: float) -> str:
    """
    Convert seconds to SRT timestamp format (HH:MM:SS,mmm).
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt(segments: List[dict], output_path: str) -> str:
    """
    Generate SRT subtitle file from transcription segments.
    
    Args:
        segments: List of segment dicts with 'start', 'end', 'text'
        output_path: Path to output .srt file
        
    Returns:
        Path to generated SRT file
    """
    # Merge short segments for better readability
    processed_segments = merge_short_segments(segments)
    
    # Generate SRT content
    srt_content = []
    
    for i, seg in enumerate(processed_segments, 1):
        # Subtitle number
        srt_content.append(str(i))
        
        # Timestamps
        start_time = format_timestamp(seg['start'])
        end_time = format_timestamp(seg['end'])
        srt_content.append(f"{start_time} --> {end_time}")
        
        # Formatted text
        formatted_text = format_japanese_text(seg['text'])
        srt_content.append(formatted_text)
        
        # Blank line between subtitles
        srt_content.append("")
    
    # Write to file with UTF-8 encoding
    output_file = Path(output_path)
    output_file.write_text("\n".join(srt_content), encoding="utf-8")
    
    print(f"\n✓ Generated SRT file: {output_file}")
    print(f"  Total subtitles: {len(processed_segments)}")
    
    return str(output_file)


def get_output_path(video_path: str) -> str:
    """
    Generate output subtitle path based on video file path.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Path for output .srt file (same location, .srt extension)
    """
    video_file = Path(video_path)
    output_path = video_file.with_suffix(config.OUTPUT_SUBTITLE_FORMAT)
    return str(output_path)


if __name__ == "__main__":
    # Test SRT generation
    test_segments = [
        {"start": 0.0, "end": 2.5, "text": "こんにちは。"},
        {"start": 3.0, "end": 6.0, "text": "本日は日本の映画を視聴しています。"},
        {"start": 6.5, "end": 10.0, "text": "これは字幕生成のテストです。"},
    ]
    
    output = "test_output.srt"
    generate_srt(test_segments, output)
    
    print("\nGenerated content:")
    print("=" * 50)
    with open(output, "r", encoding="utf-8") as f:
        print(f.read())
