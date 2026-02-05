# Qwen3-ASR Streamlit Application Guide

## Overview
Professional web interface for the Qwen3-ASR-0.6B speech recognition system.

## Features

### User Interface
- **Professional Layout**: Clean, centered design with custom styling
- **Browser Recording**: Direct microphone input via `st.audio_input`
- **Real-time Feedback**: Processing spinner during transcription
- **Prominent Display**: Transcriptions shown in editable text area
- **Auto-save**: Automatic saving to `results/` with timestamps
- **Download Option**: Download transcripts as text files

### Technical Implementation
- **Model Integration**: Uses `ASRInference` class from `src.inference`
- **GPU Acceleration**: Leverages Tesla V100 for fast transcription
- **Error Handling**: Graceful error messages for failed transcriptions
- **Caching**: Model loaded once and cached for performance

## Running the Application

### Start the Server
```bash
cd /root/ASRmodel
source venv/bin/activate
streamlit run streamlit_app.py --server.port 8501
```

### Access the Interface
Open browser to: `http://localhost:8501`

## Usage Workflow

1. **Record Audio**
   - Click "Click to record audio from your microphone"
   - Allow microphone access if prompted
   - Speak clearly into microphone
   - Click stop when finished

2. **Process Transcription**
   - Audio automatically processes when recording stops
   - Spinner shows processing status
   - Transcription appears in text area

3. **Save Results**
   - Transcript auto-saves to `results/` directory
   - Filename format: `audio_recording_YYYYMMDD_HHMMSS_transcription.txt`
   - Download button available for manual download

## File Structure

```
```
/root/ASRmodel/
├── streamlit_app.py          # Main Streamlit application
├── src/
│   └── inference.py           # ASRInference class
├── results/                   # Auto-saved transcriptions
└── data/                      # Sample audio files
```
```

## Key Components

### Page Configuration
```python
st.set_page_config(
    page_title="Qwen3-ASR Transcription",
    page_icon="🎙️",
    layout="wide"
)
```

### Audio Recording
```python
audio_data = st.audio_input("Click to record audio from your microphone")
```

### Processing Spinner
```python
with st.spinner("🔄 Processing audio and generating transcription..."):
    transcription = asr_model.transcribe(tmp_path)
```

### Auto-save Function
```python
def save_transcription(text: str, audio_filename: str = "recording") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{audio_filename}_{timestamp}_transcription.txt"
    # Saves to results/ directory
```

## Customization

### Styling
Custom CSS is embedded in the app for:
- Header formatting
- Button styling
- Color scheme
- Layout spacing

### Model Settings
Model is cached using `@st.cache_resource`:
```python
@st.cache_resource
def load_model():
    return ASRInference()
```

## Troubleshooting

### Microphone Access
- Ensure browser permissions are granted
- HTTPS or localhost required for `st.audio_input`

### Model Loading
- First run takes ~1 minute to download model
- Subsequent runs use cached model

### GPU Memory
- App uses Tesla V100 (16GB VRAM)
- Model requires ~2-3GB VRAM

## Performance

- **Model**: Qwen3-ASR-0.6B (600M parameters)
- **Device**: Tesla V100 GPU
- **Latency**: ~2-5 seconds for typical recordings
- **Memory**: ~4GB RAM + 3GB VRAM

## Auto-shutdown
The Streamlit app runs until manually stopped (Ctrl+C).
For production deployment, consider using a process manager like systemd or supervisor.