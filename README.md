# Qwen3-ASR-0.6B Automatic Speech Recognition Pipeline

A production-ready ASR pipeline leveraging the Qwen3-ASR-0.6B model for efficient speech-to-text transcription.

## Features

- 🎯 Lightweight 0.6B parameter model optimized for edge deployment
- 🚀 GPU-accelerated inference (CUDA support with CPU fallback)
- 🎵 Multi-format audio support (WAV, MP3, FLAC)
- 🔧 Automatic audio preprocessing and resampling
- 📦 Simple API with minimal configuration

## Requirements

- Python 3.8+
- CUDA-capable GPU (optional, recommended)
- 4GB+ RAM (8GB+ recommended)
- ~3GB storage for model weights

## Installation

### 1. Clone and Setup Environment

```bash
cd /root/ASRmodel
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** The installation includes PyTorch with CUDA support. For CPU-only:
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers accelerate librosa soundfile
```

## Usage

### Command-Line Interface (Recommended)

The easiest way to transcribe audio files is using the CLI:

```bash
python cli.py --audio path/to/your/audio.wav
```

**Quick Examples:**

```bash
# Transcribe the sample audio (saves to ./results/ by default)
python cli.py --audio data/OSR_us_000_0037_8k.wav

# Transcribe your own audio file
python cli.py --audio /path/to/recording.mp3

# Specify custom output directory
python cli.py --audio myfile.wav --output-dir ./my_transcriptions

# Force CPU usage
python cli.py --audio myfile.wav --device cpu

# Use custom model checkpoint
python cli.py --audio audio.flac --model-path /path/to/model
```

**CLI Options:**
- `--audio`: Path to audio file (required)
- `--output-dir`: Directory to save transcription results (default: `./results`)
- `--device`: Device (`auto`, `cuda`, or `cpu`). Default: `auto`
- `--model-path`: Model identifier or local path. Default: `Qwen/Qwen3-ASR-0.6B`
- `--help`: Show all options

### Output Files

Transcriptions are automatically saved to the specified output directory (default: `./results/`). Each transcription file is named based on the input audio file:

- Input: `myaudio.wav` → Output: `./results/myaudio_transcription.txt`
- Input: `data/recording.mp3` → Output: `./results/recording_transcription.txt`

The output directory is created automatically if it doesn't exist.

**Example Workflow:**

```bash
# Step 1: Run transcription on your audio file
python cli.py --audio /path/to/your/audio.wav

# Step 2: Check the results folder
ls -lh ./results/

# Step 3: View the transcription
cat ./results/audio_transcription.txt
```

### Quick Start (Demo)

Run the demo script to verify installation:

```bash
python demo.py
```

This will:
1. Download a sample audio file
2. Load the Qwen3-ASR-0.6B model
3. Transcribe the audio
4. Display the transcription result

### Library Usage

```python
from src.inference import QwenASRPipeline

asr = QwenASRPipeline(
    model_name="Qwen/Qwen3-ASR-0.6B",
    device="cuda"  # or "cpu"
)

transcription = asr.transcribe("path/to/audio.wav")
print(f"Transcription: {transcription}")
```

### Advanced Options

```python
transcription = asr.transcribe(
    audio_path="audio.mp3",
    language="en",  # Optional language hint
    return_timestamps=False  # Enable word-level timestamps
)
```

### Batch Processing

```python
from pathlib import Path

audio_files = Path("data").glob("*.wav")
for audio_file in audio_files:
    result = asr.transcribe(str(audio_file))
    print(f"{audio_file.name}: {result}")
```
## Project Structure

```
```
ASRmodel/
├── src/
│   └── inference.py       # ASR inference engine
├── data/                  # Sample audio files
│   └── OSR_us_000_0037_8k.wav
├── results/               # Transcription outputs (auto-created)
├── cli.py                 # Command-line interface
├── demo.py                # Verification demo
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .gitignore            # Git exclusions
```
```
- **Model:** Qwen/Qwen3-ASR-0.6B
- **Source:** https://huggingface.co/Qwen/Qwen3-ASR-0.6B
- **Parameters:** 0.6 billion
- **Architecture:** Transformer-based ASR
- **License:** Check Hugging Face model card

## Performance

- **GPU (Tesla V100):** ~0.1-0.5s per second of audio
- **CPU:** ~1-3s per second of audio
- **Memory:** ~2-3GB VRAM (GPU) / ~4GB RAM (CPU)

## Troubleshooting

### Audio File Not Found

Verify the file path is correct:
```bash
ls -lh path/to/audio.wav
python cli.py --audio "$(pwd)/audio.wav"
```

### CUDA Out of Memory

If you encounter OOM errors, use CPU mode:
```bash
python cli.py --audio audio.wav --device cpu
```

Or in Python:
```python
asr = QwenASRPipeline(model_name="Qwen/Qwen3-ASR-0.6B", device="cpu")
```

### Audio Format Not Supported

Ensure `ffmpeg` is installed for MP3/other formats:
```bash
sudo apt-get install ffmpeg
```

### Model Download Issues

If download fails, manually cache the model:
```bash
huggingface-cli download Qwen/Qwen3-ASR-0.6B
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Quality

```bash
pip install black flake8
black src/ demo.py
flake8 src/ demo.py
```

## Contributing

Contributions welcome! Please ensure:
- Code follows PEP 8 style guidelines
- New features include tests
- Documentation is updated

## License

This project uses the Qwen3-ASR-0.6B model. Please refer to the [official model card](https://huggingface.co/Qwen/Qwen3-ASR-0.6B) for licensing terms.

## Citation

If you use this pipeline in research, please cite:

```bibtex
@software{qwen3_asr_pipeline,
  title = {Qwen3-ASR-0.6B Pipeline},
  year = {2026},
  url = {https://github.com/yourusername/ASRmodel}
}
```

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review Qwen3-ASR model documentation
- Open an issue on GitHub

---

**Built with ❤️ using Qwen3-ASR-0.6B**