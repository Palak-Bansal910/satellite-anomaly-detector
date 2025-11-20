@echo off
echo Starting Telemetry Simulator...
cd /d "%~dp0.."
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
REM Set PYTHONPATH to project root so simulator module can be found
set PYTHONPATH=%CD%
REM Run from project root - simulator can now be run as script or module
python simulator\simulator.py
pause
