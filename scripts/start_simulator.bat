@echo off
echo Starting Telemetry Simulator...
cd /d "%~dp0.."
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
cd simulator
python -m simulator.simulator
pause
