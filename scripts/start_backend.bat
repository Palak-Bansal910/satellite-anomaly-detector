@echo off
echo Starting FastAPI Backend...
cd /d "%~dp0.."
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
REM Set PYTHONPATH to project root so 'backend' module can be found
set PYTHONPATH=%CD%
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload
pause
