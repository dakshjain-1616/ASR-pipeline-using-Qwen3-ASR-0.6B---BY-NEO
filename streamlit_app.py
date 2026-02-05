import streamlit as st
import os
from datetime import datetime
from pathlib import Path
import tempfile
from src.inference import QwenASRPipeline

st.set_page_config(
    page_title="Qwen3-ASR Transcription Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎙️ Qwen3-ASR Transcription Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Professional Speech-to-Text powered by Qwen3-ASR-0.6B</div>', unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with st.spinner("🔄 Loading ASR model... (first run may take a minute)"):
        return QwenASRPipeline()

def save_transcription(text: str, audio_filename: str = "recording") -> str:
    results_dir = Path("/root/ASRmodel/results")
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{audio_filename}_{timestamp}_transcription.txt"
    filepath = results_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Transcription generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Audio source: {audio_filename}\n")
        f.write("-" * 80 + "\n\n")
        f.write(text)
    
    return str(filepath)

if 'audio_input_counter' not in st.session_state:
    st.session_state.audio_input_counter = 0

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("---")
    
    st.markdown("### 🎤 Record Your Audio")
    audio_data = st.audio_input(
        "Click to record audio from your microphone",
        key=f"audio_input_{st.session_state.audio_input_counter}"
    )
    
    st.markdown("---")
    
    if audio_data is not None:
        st.audio(audio_data, format="audio/wav")
        
        with st.spinner("🔄 Processing audio and generating transcription..."):
            try:
                asr_model = load_model()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(audio_data.getvalue())
                    tmp_path = tmp_file.name
                
                transcription = asr_model.transcribe(tmp_path)
                
                os.unlink(tmp_path)
                
                if transcription and transcription.strip():
                    st.success("✅ Transcription Complete!")
                    
                    st.markdown("### 📝 Transcription Result")
                    st.text_area(
                        label="Transcribed Text",
                        value=transcription,
                        height=200,
                        disabled=False,
                        label_visibility="collapsed"
                    )
                    
                    saved_path = save_transcription(transcription, "audio_recording")
                    
                    st.info(f"💾 Transcript automatically saved to:\n`{saved_path}`")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.download_button(
                            label="⬇️ Download Transcript",
                            data=transcription,
                            file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    with col_b:
                        if st.button("🔄 Clear & Record New"):
                            st.session_state.audio_input_counter += 1
                            st.rerun()
                else:
                    st.warning("⚠️ No transcription generated. Please try recording again.")
                    
            except Exception as e:
                st.error(f"❌ Error during transcription: {str(e)}")
                st.info("Please check that your audio is clear and try again.")

st.markdown("---")

with st.expander("ℹ️ About This Application"):
    st.markdown("""
    **Qwen3-ASR Transcription Studio** leverages the state-of-the-art Qwen3-ASR-0.6B model 
    for automatic speech recognition.
    
    **Features:**
    - 🎙️ Browser-based audio recording
    - ⚡ GPU-accelerated transcription (Tesla V100)
    - 💾 Automatic transcript saving with timestamps
    - 📥 Download transcripts as text files
    - 🔄 Real-time processing feedback
    
    **Model:** Qwen/Qwen3-ASR-0.6B (0.6B parameters)
    
    **Supported Formats:** WAV, MP3, FLAC
    """)

with st.expander("🚀 Quick Start Guide"):
    st.markdown("""
    1. Click the **"Click to record audio"** button
    2. Allow microphone access if prompted
    3. Speak clearly into your microphone
    4. Click stop when finished
    5. Wait for the transcription to appear
    6. Download or save your transcript
    """)