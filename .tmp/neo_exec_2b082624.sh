cd /root/ASRmodel && timeout 15 /root/ASRmodel/venv/bin/python -c "
import sys
sys.path.insert(0, '/root/ASRmodel')
from src.inference import QwenASRPipeline
print('✓ Import successful')
print('Testing model initialization...')
asr = QwenASRPipeline()
print('✓ Model initialized successfully')
print(f'Device: {asr.device}')
" 2>&1 | head -20