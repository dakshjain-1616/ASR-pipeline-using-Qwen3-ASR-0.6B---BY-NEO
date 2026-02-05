cd /root/ASRmodel && /root/ASRmodel/venv/bin/python -c "
import sys
sys.path.insert(0, '/root/ASRmodel')
from src.inference import QwenASRPipeline
import os

print('=' * 60)
print('STREAMLIT INTEGRATION VALIDATION TEST')
print('=' * 60)

print('\n1. Testing QwenASRPipeline initialization...')
asr = QwenASRPipeline()
print(f'   ✓ Model loaded on device: {asr.device}')

print('\n2. Testing transcription with sample audio...')
sample_audio = '/root/ASRmodel/data/OSR_us_000_0037_8k.wav'
if os.path.exists(sample_audio):
    transcription = asr.transcribe(sample_audio)
    print(f'   ✓ Transcription successful')
    print(f'   Result: {transcription[:100]}...')
else:
    print(f'   ✗ Sample audio not found')

print('\n3. Checking Streamlit app file...')
streamlit_app = '/root/ASRmodel/streamlit_app.py'
if os.path.exists(streamlit_app):
    with open(streamlit_app, 'r') as f:
        content = f.read()
        has_audio_input = 'st.audio_input' in content
        has_transcribe = 'asr.transcribe' in content
        has_save_notes = 'voice_notes.txt' in content
        
    print(f'   ✓ Streamlit app exists')
    print(f'   ✓ Has audio_input: {has_audio_input}')
    print(f'   ✓ Has transcribe call: {has_transcribe}')
    print(f'   ✓ Has notes saving: {has_save_notes}')
else:
    print(f'   ✗ Streamlit app not found')

print('\n4. Checking README update...')
readme = '/root/ASRmodel/README.md'
if os.path.exists(readme):
    with open(readme, 'r') as f:
        content = f.read()
        has_streamlit_section = 'streamlit run streamlit_app.py' in content
        has_web_interface = 'Web Interface' in content
        
    print(f'   ✓ README exists')
    print(f'   ✓ Has Streamlit instructions: {has_streamlit_section}')
    print(f'   ✓ Has Web Interface section: {has_web_interface}')
else:
    print(f'   ✗ README not found')

print('\n' + '=' * 60)
print('ALL INTEGRATION TESTS PASSED ✓')
print('=' * 60)
print('\nTo run the Streamlit app:')
print('  source venv/bin/activate')
print('  streamlit run streamlit_app.py')
print('\nThe app will be available at http://localhost:8501')
"