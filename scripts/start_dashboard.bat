@echo off
echo Starting Streamlit Dashboard...
cd /d "%~dp0.."
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
cd dashboard
streamlit run streamlit_app.py --server.port 8501
pause
