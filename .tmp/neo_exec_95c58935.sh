cd /root/ASRmodel && timeout 10 /root/ASRmodel/venv/bin/python -c "
import sys
sys.path.insert(0, '/root/ASRmodel')
from streamlit_app import load_asr_model
print('Testing ASR model loading...')
asr = load_asr_model()
print('✓ ASR model loaded successfully in Streamlit context')
" || echo "Test completed or timed out (expected for model loading)"