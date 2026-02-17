"""
Japanese text formatting for subtitle display
"""

import re
from typing import List
import config


# Japanese punctuation marks
JAPANESE_PUNCTUATION = "。、！？…‥「」『』（）【】"
SENTENCE_ENDERS = "。！？"


def format_japanese_text(text: str, max_line_length: int = None) -> str:
    """
    Format Japanese text with proper line breaking.
    
    Args:
        text: Japanese text to format
        max_line_length: Maximum characters per line (default from config)
    
    Returns:
        Formatted text with line breaks
    """
    if max_line_length is None:
        max_line_length = config.MAX_LINE_LENGTH
    
    # Remove extra whitespace
    text = text.strip()
    
    # If text is short enough, return as-is
    if len(text) <= max_line_length:
        return text
    
    # If text can fit in 2 lines
    if len(text) <= max_line_length * config.MAX_LINES_PER_SUBTITLE:
        return _split_into_lines(text, max_line_length)
    
    # Text is too long, truncate with ellipsis
    truncated = text[:max_line_length * config.MAX_LINES_PER_SUBTITLE - 1] + "…"
    return _split_into_lines(truncated, max_line_length)


def _split_into_lines(text: str, max_length: int) -> str:
    """
    Split Japanese text into multiple lines intelligently.
    
    Prioritizes breaking at:
    1. Sentence endings (。！？)
    2. Clause boundaries (、)
    3. Other punctuation
    4. Natural word boundaries
    
    Args:
        text: Text to split
        max_length: Maximum length per line
        
    Returns:
        Text with newline characters
    """
    if len(text) <= max_length:
        return text
    
    # Try to find a good break point in the first half
    ideal_break = max_length
    
    # Look for punctuation near the ideal break point
    search_start = max(0, ideal_break - 10)
    search_end = min(len(text), ideal_break + 10)
    search_region = text[search_start:search_end]
    
    # Priority 1: Sentence enders
    for punct in SENTENCE_ENDERS:
        if punct in search_region:
            pos = search_region.rfind(punct)
            if pos != -1:
                break_pos = search_start + pos + 1
                line1 = text[:break_pos].strip()
                line2 = text[break_pos:].strip()
                return line1 + "\n" + line2
    
    # Priority 2: Reading punctuation (、)
    if "、" in search_region:
        pos = search_region.rfind("、")
        if pos != -1:
            break_pos = search_start + pos + 1
            line1 = text[:break_pos].strip()
            line2 = text[break_pos:].strip()
            return line1 + "\n" + line2
    
    # Priority 3: Any Japanese punctuation
    for i in range(len(search_region) - 1, -1, -1):
        if search_region[i] in JAPANESE_PUNCTUATION:
            break_pos = search_start + i + 1
            line1 = text[:break_pos].strip()
            line2 = text[break_pos:].strip()
            return line1 + "\n" + line2
    
    # Priority 4: Break at ideal position (no good punctuation found)
    line1 = text[:ideal_break].strip()
    line2 = text[ideal_break:].strip()
    return line1 + "\n" + line2


def merge_short_segments(segments: List[dict]) -> List[dict]:
    """
    Merge segments that are too short into longer, more readable subtitles.
    
    Args:
        segments: List of segment dicts with 'start', 'end', 'text'
        
    Returns:
        Merged segments list
    """
    if not segments:
        return []
    
    merged = []
    current = None
    
    for seg in segments:
        duration = seg['end'] - seg['start']
        
        # If no current segment, start with this one
        if current is None:
            current = seg.copy()
            continue
        
        # Calculate gap between segments
        gap = seg['start'] - current['end']
        
        # Merge if:
        # - Current is too short AND
        # - Gap is small AND
        # - Combined text is not too long
        should_merge = (
            (current['end'] - current['start']) < config.MIN_SUBTITLE_DURATION and
            gap < 1.0 and  # Less than 1 second gap
            len(current['text'] + seg['text']) <= config.MAX_LINE_LENGTH * config.MAX_LINES_PER_SUBTITLE
        )
        
        if should_merge:
            # Merge segments
            current['end'] = seg['end']
            current['text'] = current['text'] + seg['text']
        else:
            # Save current and start new one
            merged.append(current)
            current = seg.copy()
    
    # Don't forget the last segment
    if current is not None:
        merged.append(current)
    
    return merged


if __name__ == "__main__":
    # Test formatting
    test_texts = [
        "こんにちは。",
        "こんにちは。本日は日本の映画を視聴しています。",
        "これは非常に長いテキストの例です。日本語の字幕は適切な位置で改行する必要があります。句読点を考慮して、読みやすい形式にする必要があります。",
    ]
    
    print("Testing Japanese text formatting:")
    print("=" * 50)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}:")
        print(f"Original: {text}")
        print(f"Formatted:\n{format_japanese_text(text)}")
        print("-" * 50)
