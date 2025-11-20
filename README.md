# Project Overview
This system simulates satellite telemetry, detects anomalies using a FastAPI backend, 
stores them in SQLite, and visualizes results in a Streamlit dashboard.

## Project Structure
project/
│-- backend/
│   │-- core/
│   │-- routes/
│   │-- models/
│   │-- schemas/
│   │-- services/
│   │-- main.py
│-- dashboard/
│-- simulator/
│-- scripts/
│   │-- start_backend.sh
│   │-- start_dashboard.sh
│   │-- start_simulator.sh
│-- data/
│-- requirements.txt
│-- Dockerfile
│-- .env

# Setup & Installation
 # 1. Install dependencies
pip install -r backend/requirements.txt
 # 2.creation of .env file
DB_URL=sqlite:///./data/anomalies.db
# Start backend
bash scripts/start_backend.sh
# Start dashboard
bash scripts/start_dashboard.sh
# Start simulator
bash scripts/start_simulator.sh
# Docker
docker build -t anomaly-backend .
docker run -p 8000:8000 anomaly-backend

# Architecture Diagram

docker build -t anomaly-backend .
docker run -p 8000:8000 anomaly-backend
