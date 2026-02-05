ls -la /root/ASRmodel/venv/bin/ | head -20
which /usr/bin/python3
/root/ASRmodel/venv/bin/python3 -c "import sys; print(sys.executable); import streamlit; print(f'Streamlit: {streamlit.__version__}')"