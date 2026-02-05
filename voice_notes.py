import argparse
import logging
import sys
import numpy as np
import soundfile as sf
from pathlib import Path
from datetime import datetime
from src.inference import QwenASRPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class VoiceNotesApp:
    """
    Real-time voice notes application with chunk-based transcription.
    """
    
    def __init__(
        self,
        output_file: str = "voice_notes.txt",
        chunk_duration: float = 5.0
    ):
        """
        Initialize the Voice Notes application.
        
        Args:
            output_file: Path to the output text file
            chunk_duration: Duration of each audio chunk in seconds
        """
        self.output_file = output_file
        self.chunk_duration = chunk_duration
        self.pipeline = None
        
        logger.info("Initializing Voice Notes Application")
        logger.info(f"Output file: {self.output_file}")
        logger.info(f"Chunk duration: {self.chunk_duration}s")
    
    def initialize_pipeline(self):
        """
        Initialize the ASR pipeline.
        """
        if self.pipeline is None:
            logger.info("Loading ASR model...")
            self.pipeline = QwenASRPipeline()
            logger.info("ASR model loaded successfully")
    
    def append_transcription(self, text: str):
        """
        Append transcription to the output file with timestamp.
        
        Args:
            text: Transcribed text
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.output_file, "a") as f:
            f.write(f"[{timestamp}] {text}\n")
        logger.info(f"Appended to {self.output_file}")
    
    def process_audio_chunk(self, audio_chunk: np.ndarray, sampling_rate: int):
        """
        Process a single audio chunk and transcribe it.
        
        Args:
            audio_chunk: Audio data as numpy array
            sampling_rate: Sampling rate of the audio
        """
        try:
            if len(audio_chunk) == 0:
                logger.warning("Empty audio chunk, skipping")
                return
            
            logger.info(f"Processing chunk: {len(audio_chunk)} samples at {sampling_rate}Hz")
            
            transcription = self.pipeline.transcribe_numpy(
                audio_array=audio_chunk,
                sampling_rate=sampling_rate
            )
            
            if transcription.strip():
                print(f"\n[TRANSCRIPTION] {transcription}")
                self.append_transcription(transcription)
            else:
                logger.info("Empty transcription, skipping")
                
        except Exception as e:
            logger.error(f"Failed to process audio chunk: {str(e)}")
    
    def simulate_from_file(self, audio_file: str):
        """
        Simulate real-time audio capture from a file.
        
        Args:
            audio_file: Path to audio file to simulate streaming from
        """
        audio_path = Path(audio_file)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        logger.info(f"Simulating audio stream from: {audio_file}")
        
        audio_data, sampling_rate = sf.read(audio_file)
        
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)
        
        total_duration = len(audio_data) / sampling_rate
        chunk_samples = int(self.chunk_duration * sampling_rate)
        
        logger.info(f"Audio info: {len(audio_data)} samples, {sampling_rate}Hz, {total_duration:.2f}s total")
        logger.info(f"Processing in chunks of {self.chunk_duration}s ({chunk_samples} samples)")
        
        self.initialize_pipeline()
        
        num_chunks = int(np.ceil(len(audio_data) / chunk_samples))
        logger.info(f"Starting streaming simulation ({num_chunks} chunks)...")
        
        for i in range(num_chunks):
            start_idx = i * chunk_samples
            end_idx = min(start_idx + chunk_samples, len(audio_data))
            chunk = audio_data[start_idx:end_idx]
            
            logger.info(f"\n--- Chunk {i+1}/{num_chunks} ---")
            self.process_audio_chunk(chunk, sampling_rate)
        
        logger.info("\nStreaming simulation complete!")
    
    def run_microphone_capture(self):
        """
        Run real-time microphone capture (requires pyaudio).
        """
        try:
            import pyaudio
        except ImportError:
            logger.error("PyAudio not installed. Install with: pip install pyaudio")
            logger.info("Alternatively, use --simulate-input <file> to test with an audio file")
            sys.exit(1)
        
        logger.info("Starting microphone capture...")
        logger.info("Press Ctrl+C to stop")
        
        self.initialize_pipeline()
        
        p = pyaudio.PyAudio()
        
        sampling_rate = 16000
        chunk_samples = int(self.chunk_duration * sampling_rate)
        
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=sampling_rate,
            input=True,
            frames_per_buffer=chunk_samples
        )
        
        try:
            chunk_count = 0
            while True:
                audio_chunk = stream.read(chunk_samples, exception_on_overflow=False)
                audio_array = np.frombuffer(audio_chunk, dtype=np.float32)
                
                chunk_count += 1
                logger.info(f"\n--- Chunk {chunk_count} ---")
                self.process_audio_chunk(audio_array, sampling_rate)
                
        except KeyboardInterrupt:
            logger.info("\nStopping microphone capture...")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            logger.info("Microphone capture stopped")


def main():
    """
    Main entry point for the Voice Notes application.
    """
    parser = argparse.ArgumentParser(
        description="Real-time Voice Notes Application with ASR"
    )
    parser.add_argument(
        "--simulate-input",
        type=str,
        default=None,
        help="Simulate audio stream from a file instead of using microphone"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="voice_notes.txt",
        help="Output text file for transcriptions (default: voice_notes.txt)"
    )
    parser.add_argument(
        "--chunk-duration",
        type=float,
        default=5.0,
        help="Duration of each audio chunk in seconds (default: 5.0)"
    )
    
    args = parser.parse_args()
    
    app = VoiceNotesApp(
        output_file=args.output,
        chunk_duration=args.chunk_duration
    )
    
    try:
        if args.simulate_input:
            app.simulate_from_file(args.simulate_input)
        else:
            app.run_microphone_capture()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()