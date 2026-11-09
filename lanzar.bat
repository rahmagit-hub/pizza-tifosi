@echo off
cd /d "%~dp0"
pip install streamlit pandas plotly
streamlit run app.py
pause