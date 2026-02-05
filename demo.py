import sys
import time
from pathlib import Path
import urllib.request

sys.path.insert(0, str(Path(__file__).parent / "src"))

from inference import QwenASRPipeline


def download_sample_audio(url: str, save_path: Path) -> Path:
    """
    Download sample audio file for demonstration.
    
    Args:
        url: URL to download audio from
        save_path: Path to save the audio file
        
    Returns:
        Path to downloaded file
    """
    print(f"Downloading sample audio from: {url}")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    urllib.request.urlretrieve(url, save_path)
    print(f"Audio saved to: {save_path}")
    return save_path


def main():
    """
    Demonstrate the Qwen ASR pipeline functionality.
    """
    print("=" * 80)
    print("Qwen3-ASR-0.6B Demonstration")
    print("=" * 80)
    print()
    
    sample_audio_url = "https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/1.flac"
    audio_file = Path(__file__).parent / "data" / "sample_audio.flac"
    
    try:
        if not audio_file.exists():
            audio_file = download_sample_audio(sample_audio_url, audio_file)
        else:
            print(f"Using existing audio file: {audio_file}")
        
        print()
        print("-" * 80)
        print("Initializing ASR Pipeline")
        print("-" * 80)
        print()
        
        pipeline = QwenASRPipeline()
        
        print()
        print("-" * 80)
        print("Running Transcription")
        print("-" * 80)
        print()
        
        start_time = time.time()
        transcription = pipeline.transcribe(audio_file)
        execution_time = time.time() - start_time
        
        print()
        print("=" * 80)
        print("RESULTS")
        print("=" * 80)
        print(f"\nTranscription: {transcription}")
        print(f"\nExecution Time: {execution_time:.2f} seconds")
        print()
        
        if transcription and len(transcription) > 0:
            print("✓ SUCCESS: Transcription completed successfully!")
        else:
            print("✗ WARNING: Transcription returned empty result")
        
        print("=" * 80)
        
    except Exception as e:
        print()
        print("=" * 80)
        print("ERROR")
        print("=" * 80)
        print(f"\nAn error occurred: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()