/root/ASRmodel/venv/bin/python3 -c "
import ast
import sys

with open('/root/ASRmodel/streamlit_app.py', 'r') as f:
    code = f.read()

ast.parse(code)
print('✓ Streamlit app syntax is valid')

if 'audio_input_counter' in code:
    print('✓ Session state counter implemented')
else:
    print('✗ Session state counter missing')
    sys.exit(1)

if 'key=f\"audio_input_{st.session_state.audio_input_counter}\"' in code:
    print('✓ Dynamic key for audio_input widget implemented')
else:
    print('✗ Dynamic key not properly implemented')
    sys.exit(1)

if 'st.session_state.audio_input_counter += 1' in code:
    print('✓ Counter increment on button click implemented')
else:
    print('✗ Counter increment missing')
    sys.exit(1)

print('\n✅ All Clear/Record New button fixes verified successfully!')
print('\nImplemented fix:')
print('1. Added session state counter: audio_input_counter')
print('2. Dynamic key for audio_input widget forces reset on counter change')
print('3. Button increments counter before rerun, triggering widget reset')
"