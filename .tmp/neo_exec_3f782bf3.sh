echo "=== FINAL VERIFICATION ==="
echo ""
echo "1. Checking upgraded inference.py has transcribe_numpy method:"
grep -A 5 "def transcribe_numpy" /root/ASRmodel/src/inference.py | head -6
echo ""
echo "2. Verifying voice_notes.py exists and has key features:"
ls -lh /root/ASRmodel/voice_notes.py
grep -E "(--simulate-input|save_transcription|process_audio_chunk)" /root/ASRmodel/voice_notes.py | head -3
echo ""
echo "3. Checking voice_notes.txt output with timestamps:"
head -4 /root/ASRmodel/voice_notes.txt
echo ""
echo "4. Running quick test to confirm end-to-end functionality:"
cd /root/ASRmodel && /root/ASRmodel/venv/bin/python voice_notes.py --simulate-input data/OSR_us_000_0037_8k.wav --chunk-duration 10.0 2>&1 | grep -E "(TRANSCRIPTION|Processing chunk|voice_notes.txt)" | head -10