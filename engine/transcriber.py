"""
Japanese transcription engine using faster-whisper
"""

from faster_whisper import WhisperModel
from typing import List, Dict, Callable, Optional
import time

import config
from .hardware import get_device_config


class JapaneseTranscriber:
    """
    High-performance Japanese transcription using faster-whisper with kotoba model.
    """
    
    def __init__(self, progress_callback: Optional[Callable[[float, str], None]] = None):
        """
        Initialize the transcriber with faster-whisper model.
        
        Args:
            progress_callback: Optional callback function(progress, status_message)
        """
        self.progress_callback = progress_callback
        self.model = None
        
    def load_model(self) -> None:
        """
        Load the faster-whisper model with optimal hardware settings.
        """
        if self.model is not None:
            return  # Already loaded
        
        self._update_progress(0.0, "Detecting hardware...")
        device, compute_type = get_device_config()
        
        self._update_progress(0.1, f"Loading model: {config.MODEL_NAME}...")
        print(f"\nLoading model: {config.MODEL_NAME}")
        print(f"Device: {device}, Compute type: {compute_type}")
        
        try:
            self.model = WhisperModel(
                config.MODEL_NAME,
                device=device,
                compute_type=compute_type,
                num_workers=1,  # Single worker to avoid multiprocessing issues  
                download_root=None,
            )
            print("✓ Model loaded successfully")
            self._update_progress(0.2, "Model loaded")
            
        except Exception as e:
            error_msg = f"Failed to load model: {e}"
            self._update_progress(0.0, error_msg)
            raise RuntimeError(error_msg)
    
    def transcribe(self, audio_path: str) -> List[Dict]:
        """
        Transcribe audio file to Japanese text with timestamps.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            List of segments with 'start', 'end', and 'text' keys
        """
        if self.model is None:
            self.load_model()
        
        self._update_progress(0.2, "Starting transcription...")
        print(f"\nTranscribing: {audio_path}")
        print(f"Language: {config.LANGUAGE}")
        print(f"Beam size: {config.BEAM_SIZE}")
        print(f"Initial prompt: {config.INITIAL_PROMPT}")
        
        start_time = time.time()
        
        try:
            # Get audio info for progress tracking
            import wave
            with wave.open(audio_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                duration = frames / float(rate)
            
            print(f"\nDetected language: {config.LANGUAGE}")
            print(f"Duration: {duration:.2f} seconds")
            
            # Transcribe with optimized parameters
            # Enable VAD for performance (config.VAD_FILTER handles platform safety)
            transcribe_options = {
                "language": config.LANGUAGE,
                "beam_size": config.BEAM_SIZE,
                "temperature": config.TEMPERATURE,
                "initial_prompt": config.INITIAL_PROMPT,
                "vad_filter": config.VAD_FILTER,
                "word_timestamps": False,
            }

            # Only add vad_parameters if VAD is enabled to avoid potential issues
            if config.VAD_FILTER:
                transcribe_options["vad_parameters"] = config.VAD_PARAMETERS

            segments_generator, info = self.model.transcribe(
                audio_path,
                **transcribe_options
            )
            
            print(f"\nProcessing segments...")
            
            # Process segments
            result_segments = []
            processed_time = 0.0
            
            for segment in segments_generator:
                result_segments.append({
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text.strip(),
                })
                
                # Update progress based on time processed
                processed_time = segment.end
                progress = 0.2 + (0.7 * (processed_time / duration))
                self._update_progress(
                    min(progress, 0.9),
                    f"Processing: {processed_time:.0f}s / {duration:.0f}s"
                )
            
            elapsed_time = time.time() - start_time
            rtf = elapsed_time / duration if duration > 0 else 0
            
            print(f"\n✓ Transcription complete!")
            print(f"  Segments: {len(result_segments)}")
            print(f"  Time: {elapsed_time:.2f}s (RTF: {rtf:.2f}x)")
            
            self._update_progress(0.9, f"Transcribed {len(result_segments)} segments")
            
            return result_segments
            
        except Exception as e:
            error_msg = f"Transcription failed: {e}"
            self._update_progress(0.0, error_msg)
            raise RuntimeError(error_msg)
    
    def _update_progress(self, progress: float, message: str) -> None:
        """
        Update progress via callback if provided.
        
        Args:
            progress: Float between 0.0 and 1.0
            message: Status message
        """
        if self.progress_callback:
            self.progress_callback(progress, message)


if __name__ == "__main__":
    # Test transcription
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python transcriber.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    transcriber = JapaneseTranscriber()
    segments = transcriber.transcribe(audio_file)
    
    print("\n" + "=" * 50)
    print("TRANSCRIPTION RESULTS:")
    print("=" * 50)
    
    for i, seg in enumerate(segments[:5], 1):  # Show first 5
        print(f"\n[{i}] {seg['start']:.2f}s - {seg['end']:.2f}s")
        print(f"    {seg['text']}")
    
    if len(segments) > 5:
        print(f"\n... and {len(segments) - 5} more segments")
