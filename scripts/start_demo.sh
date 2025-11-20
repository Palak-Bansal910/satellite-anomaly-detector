#!/usr/bin/env bash

########################################
# Satellite Anomaly Detector – Demo Run
# Usage (from project root):
#   bash start_demo.sh
########################################

# Always run from the script's folder (project root)
cd "$(dirname "$0")"

# ----- CONFIG -----
BACKEND_PORT=8000
DASHBOARD_PORT=8501

echo "========== SATELLITE ANOMALY DETECTOR DEMO =========="
echo "Project root : $(pwd)"
echo "Backend port : $BACKEND_PORT"
echo "Dashboard    : http://localhost:$DASHBOARD_PORT"
echo "====================================================="
echo

# 1) Start FastAPI backend
echo "[1/3] Starting FastAPI backend on port $BACKEND_PORT ..."
(
  cd backend || exit 1
  uvicorn api.main:app --reload --port "$BACKEND_PORT"
) &

BACKEND_PID=$!
echo "    -> Backend PID: $BACKEND_PID"
sleep 5

# 2) Start telemetry simulator  (comment this block if you don't want simulator)
echo "[2/3] Starting telemetry simulator ..."
(
  cd simulator || exit 1
  python -m simulator.simulator
) &

SIM_PID=$!
echo "    -> Simulator PID: $SIM_PID"
sleep 5

# 3) Start Streamlit dashboard
echo "[3/3] Starting Streamlit dashboard on port $DASHBOARD_PORT ..."
(
  cd dashboard || exit 1
  streamlit run streamlit_app.py --server.port "$DASHBOARD_PORT"
) &

DASH_PID=$!
echo "    -> Dashboard PID: $DASH_PID"
echo
echo "All services started."
echo "Backend   : http://127.0.0.1:$BACKEND_PORT"
echo "Dashboard : http://localhost:$DASHBOARD_PORT"
echo
echo "Press Ctrl+C to stop all demo processes."
echo "====================================================="

# Wait here; when you Ctrl+C, kill child processes
trap "echo 'Stopping demo...'; kill $BACKEND_PID $SIM_PID $DASH_PID 2>/dev/null; exit 0" INT

# Keep script alive so children keep running
while true; do
  sleep 2
done
