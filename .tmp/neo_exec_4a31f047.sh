cd /root/ASRmodel && ./venv/bin/python cli.py --audio data/sample_audio.flac 2>&1 | tee cli_verification.log
cat cli_verification.log