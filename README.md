# Qwen3-ASR-0.6B Automatic Speech Recognition Pipeline by NEO

## 🎯 How NEO Tackled the Problem

Speech recognition on edge devices requires balancing accuracy, speed, and resource constraints:

- **Edge Device Constraints**: Full-size ASR models (1B+ parameters) are too heavy for edge deployment. NEO selected the Qwen3-ASR-0.6B model, achieving production-quality transcription with only 0.6B parameters and ~3GB storage footprint.

- **Hardware Flexibility**: Users have varying hardware setups (GPU/CPU, local/remote). NEO implemented automatic device detection with CUDA acceleration and CPU fallback, ensuring seamless operation across environments.

- **Audio Format Compatibility**: Real-world audio comes in multiple formats (WAV, MP3, FLAC) with varying sample rates. NEO integrated librosa-based preprocessing with automatic resampling, handling format conversion transparently.

- **Remote Server Accessibility**: Server-based ASR typically requires audio hardware on the backend. NEO built a Streamlit web interface with browser-based microphone recording, bypassing server-side audio dependencies entirely.

- **Production Usability**: Research models often lack user-friendly interfaces. NEO created both a CLI for batch processing and a web UI for interactive use, with automatic output management and clear error handling.

## Features

- 🎯 Lightweight 0.6B parameter model optimized for edge deployment
- 🚀 GPU-accelerated inference (CUDA support with CPU fallback)
- 🎵 Multi-format audio support (WAV, MP3, FLAC)
- 🔧 Automatic audio preprocessing and resampling
- 📦 Simple API with minimal configuration
- 🌐 Browser-based recording via Streamlit web interface

## Quick Start
```bash
# Setup
cd /root/ASRmodel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Web Interface (Recommended)
streamlit run streamlit_app.py

# CLI Usage
python cli.py --audio data/OSR_us_000_0037_8k.wav
```

## 📡 Usage

### Web Interface
```bash
streamlit run streamlit_app.py
```

Features:
- Record audio directly in browser
- Instant transcription display
- Auto-save to `voice_notes.txt`
- No server-side audio hardware needed

**Remote Server:** Use SSH port forwarding:
```bash
ssh -L 8501:localhost:8501 user@server
```

### Command-Line Interface
```bash
# Basic transcription
python cli.py --audio path/to/audio.wav

# Custom output directory
python cli.py --audio audio.mp3 --output-dir ./transcriptions

# Force CPU usage
python cli.py --audio audio.flac --device cpu
```

### Python API
```python
from src.inference import QwenASRPipeline

asr = QwenASRPipeline(model_name="Qwen/Qwen3-ASR-0.6B", device="cuda")
transcription = asr.transcribe("audio.wav")
print(transcription)
```

## 📊 Performance

- **GPU (Tesla V100):** ~0.1-0.5s per second of audio
- **CPU:** ~1-3s per second of audio
- **Memory:** ~2-3GB VRAM (GPU) / ~4GB RAM (CPU)

## 🔧 Extending with NEO

Enhance this ASR pipeline using **NEO**, an AI-powered development assistant:

### Getting Started with NEO

1. **Install the NEO VS Code Extension**
   
   [**NEO VS Code Extension**](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)

2. **Use NEO to Extend Functionality**
   
   - **Multi-language support**: Add language detection and multilingual transcription
   - **Speaker diarization**: Identify and separate multiple speakers in audio
   - **Real-time streaming**: Implement WebSocket-based live transcription
   - **Custom vocabulary**: Add domain-specific terms for medical/legal/technical use
   - **Noise reduction**: Integrate audio enhancement for noisy environments
   - **Batch processing**: Create parallel processing for large audio datasets
   - **REST API**: Build FastAPI endpoints for production deployment
   - **Subtitle generation**: Auto-generate SRT/VTT files with timestamps

3. **Example NEO Prompts**
```
   "Add speaker diarization to identify multiple speakers in conversations"
   
   "Create a FastAPI endpoint for remote transcription requests"
   
   "Implement real-time streaming transcription via WebSocket"
   
   "Add support for Spanish and French language transcription"
   
   "Build a batch processing script for transcribing entire directories"
   
   "Integrate noise reduction preprocessing using noisereduce library"
   
   "Create SRT subtitle file generation with word-level timestamps"
   
   "Add confidence scoring for transcription quality assessment"
```

4. **Advanced Use Cases**
   
   - **Meeting Transcription**: Build automated meeting notes with speaker labels
   - **Podcast Production**: Create searchable transcripts for audio content
   - **Accessibility Tools**: Generate live captions for video streaming
   - **Call Center Analytics**: Transcribe and analyze customer support calls
   - **Legal Documentation**: Transcribe court proceedings and depositions
   - **Medical Dictation**: Convert doctor notes to structured EHR entries
   - **Language Learning**: Build pronunciation assessment tools
   - **Voice Search**: Enable voice-controlled application interfaces

### Learn More About NEO

Visit [heyneo.so](https://heyneo.so/) to explore additional features.

## 📂 Project Structure
```
ASRmodel/
├── src/
│   └── inference.py       # ASR inference engine
├── data/                  # Sample audio files
├── results/               # Transcription outputs
├── cli.py                 # Command-line interface
├── streamlit_app.py       # Web interface
├── demo.py                # Verification demo
└── requirements.txt       # Dependencies
```

## 🐛 Troubleshooting

**CUDA Out of Memory:**
```bash
python cli.py --audio audio.wav --device cpu
```

**Audio Format Issues:**
```bash
sudo apt-get install ffmpeg
```

**Model Download:**
```bash
huggingface-cli download Qwen/Qwen3-ASR-0.6B
```

## 📜 License

Uses Qwen3-ASR-0.6B model. See [model card](https://huggingface.co/Qwen/Qwen3-ASR-0.6B) for licensing.

---

**Built with ❤️ using Qwen3-ASR-0.6B**
