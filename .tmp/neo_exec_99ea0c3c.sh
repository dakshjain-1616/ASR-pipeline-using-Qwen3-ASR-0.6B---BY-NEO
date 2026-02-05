cd /root/ASRmodel && source /root/ASRmodel/venv/bin/activate 2>/dev/null || /usr/bin/python3 -m venv venv
source /root/ASRmodel/venv/bin/activate && pip install --upgrade pip
source /root/ASRmodel/venv/bin/activate && pip install transformers torch torchaudio librosa scipy accelerate soundfile
/usr/bin/python3 -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"}')"