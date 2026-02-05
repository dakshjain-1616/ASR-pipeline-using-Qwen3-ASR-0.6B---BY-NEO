import argparse
import sys
import os
from pathlib import Path
import torch
import torchaudio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent / "src"))
from inference import QwenASRPipeline

def main():
    parser = argparse.ArgumentParser(
        description='Qwen3-ASR-0.6B: Automatic Speech Recognition CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python cli.py --audio data/sample_audio.flac
  python cli.py --audio /path/to/your/audio.wav
  python cli.py --audio recording.mp3 --device cpu
  python cli.py --audio myaudio.wav --output-dir ./my_results
        '''
    )
    
    parser.add_argument(
        '--audio',
        type=str,
        required=True,
        help='Path to audio file (supports WAV, MP3, FLAC, etc.)'
    )
    
    parser.add_argument(
        '--device',
        type=str,
        default='auto',
        choices=['auto', 'cuda', 'cpu'],
        help='Device to run inference on (default: auto - uses CUDA if available)'
    )
    
    parser.add_argument(
        '--model-path',
        type=str,
        default='Qwen/Qwen3-ASR-0.6B',
        help='HuggingFace model identifier or local path (default: Qwen/Qwen3-ASR-0.6B)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./results',
        help='Directory to save transcription results (default: ./results)'
    )
    
    args = parser.parse_args()
    
    audio_path = Path(args.audio)
    if not audio_path.exists():
        logger.error(f"Audio file not found: {args.audio}")
        sys.exit(1)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_dir.absolute()}")
    
    if args.device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = args.device
    
    logger.info(f"Loading ASR model: {args.model_path}")
    logger.info(f"Using device: {device}")
    
    try:
        asr = QwenASRPipeline(model_name=args.model_path, device=device)
        logger.info(f"Processing audio file: {audio_path}")
        
        transcription = asr.transcribe(str(audio_path))
        
        output_filename = audio_path.stem + "_transcription.txt"
        output_path = output_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcription)
        
        print("\n" + "="*60)
        print("TRANSCRIPTION RESULT")
        print("="*60)
        print(transcription)
        print("="*60)
        print(f"\n✓ Transcription saved to: {output_path.absolute()}\n")
        
        logger.info(f"Transcription saved to: {output_path}")
        logger.info("Transcription completed successfully")
        
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()