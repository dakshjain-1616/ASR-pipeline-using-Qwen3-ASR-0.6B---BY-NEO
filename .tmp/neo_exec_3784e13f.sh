echo "=== Verifying All Deliverables ==="
echo ""
echo "1. ASR Inference Engine (src/inference.py):"
ls -lh /root/ASRmodel/src/inference.py
echo ""
echo "2. Demo Verification Script (demo.py):"
ls -lh /root/ASRmodel/demo.py
echo ""
echo "3. Voice Notes Application (voice_notes.py):"
ls -lh /root/ASRmodel/voice_notes.py
echo ""
echo "4. Voice Notes Output (voice_notes.txt):"
ls -lh /root/ASRmodel/voice_notes.txt
wc -l /root/ASRmodel/voice_notes.txt
echo ""
echo "5. Sample Audio Files:"
ls -lh /root/ASRmodel/data/
echo ""
echo "=== Verification Complete ==="