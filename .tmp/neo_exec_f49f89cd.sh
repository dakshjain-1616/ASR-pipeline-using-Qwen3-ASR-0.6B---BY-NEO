source /root/ASRmodel/venv/bin/activate && /usr/bin/python3 -c "
import sys
sys.path.insert(0, '/root/ASRmodel')
from src.inference import QwenASRPipeline
print('✓ QwenASRPipeline imported successfully')
"