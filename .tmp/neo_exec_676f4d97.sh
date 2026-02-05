source /root/ASRmodel/venv/bin/activate && /usr/bin/python3 << 'EOF'
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/root/ASRmodel')

results_dir = Path("/root/ASRmodel/results")
results_dir.mkdir(exist_ok=True)

def save_transcription(text: str, audio_filename: str = "recording") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{audio_filename}_{timestamp}_transcription.txt"
    filepath = results_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Transcription generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Audio source: {audio_filename}\n")
        f.write("-" * 80 + "\n\n")
        f.write(text)
    
    return str(filepath)

test_text = "This is a test transcription from the refactored Streamlit UI."
saved_path = save_transcription(test_text, "test_recording")

print(f"✓ Test transcription saved to: {saved_path}")
print(f"✓ File exists: {Path(saved_path).exists()}")

with open(saved_path, 'r') as f:
    content = f.read()
    if test_text in content:
        print(f"✓ Content verified")
    else:
        print(f"✗ Content mismatch")

print("\nSaved transcriptions in results/:")
for item in sorted(results_dir.glob("*.txt")):
    print(f"  - {item.name}")
EOF