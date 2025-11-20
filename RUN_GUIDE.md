# Step-by-Step Guide: Running Satellite Anomaly Detector

This guide will walk you through setting up and running the Satellite Anomaly Detection system on Windows or Linux/Mac.

## ⚡ Quick Start (TL;DR)

1. **Install dependencies:** `pip install -r requirements.txt`
2. **Start backend:** Double-click `scripts\start_backend.bat` (Windows) or run `cd backend && python -m uvicorn api.main:app --port 8000 --reload`
3. **Start simulator:** Double-click `scripts\start_simulator.bat` (Windows) or run `cd simulator && python -m simulator.simulator`
4. **Start dashboard:** Double-click `scripts\start_dashboard.bat` (Windows) or run `cd dashboard && streamlit run streamlit_app.py`
5. **Open browser:** Go to http://localhost:8501

**Detailed instructions below** ⬇️

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.8 or higher** installed
- **pip** (Python package installer)
- A terminal/command prompt (PowerShell, CMD, Git Bash, or Terminal)

## 🔧 Step 1: Check Python Installation

Open your terminal/command prompt and verify Python is installed:

```bash
python --version
# or
python3 --version
```

You should see something like `Python 3.8.x` or higher.

## 📦 Step 2: Navigate to Project Directory

Navigate to the project root directory:

```bash
cd "C:\Users\hp\OneDrive\Desktop\spotted new\check\new\Spotted\ridhima\satellite-anomaly-detector"
```

**For Windows (PowerShell/CMD):**
```powershell
cd "C:\Users\hp\OneDrive\Desktop\spotted new\check\new\Spotted\ridhima\satellite-anomaly-detector"
```

**For Linux/Mac or Git Bash:**
```bash
cd "/c/Users/hp/OneDrive/Desktop/spotted new/check/new/Spotted/ridhima/satellite-anomaly-detector"
```

## 🎯 Step 3: Create Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac/Git Bash:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt after activation.

## 📚 Step 4: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (backend framework)
- Uvicorn (ASGI server)
- Streamlit (dashboard framework)
- TensorFlow (ML models)
- Plotly (visualizations)
- And other dependencies

**Note:** TensorFlow installation may take several minutes. Be patient!

## 🚀 Step 5: Running the Project

The project consists of **3 main components** that need to run simultaneously:

1. **FastAPI Backend** (Port 8000) - Processes telemetry and detects anomalies
2. **Simulator** - Generates synthetic satellite telemetry data
3. **Streamlit Dashboard** (Port 8501) - Visualizes anomalies

### Option A: Run All Services Together (Recommended)

**Windows (Easiest - Double-click batch files):**

Simply double-click these batch files in order (in the `scripts` folder):
1. `start_backend.bat` - Wait for it to start (you'll see "Application startup complete")
2. `start_simulator.bat` - This will start sending telemetry
3. `start_dashboard.bat` - This will open your browser automatically

**Windows (PowerShell - 3 separate terminals):**

Open **3 separate PowerShell windows** and run each command:

**Terminal 1 - Backend:**
```powershell
cd "C:\Users\hp\OneDrive\Desktop\spotted new\check\new\Spotted\ridhima\satellite-anomaly-detector"
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH = $PWD
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 - Simulator:**
```powershell
cd "C:\Users\hp\OneDrive\Desktop\spotted new\check\new\Spotted\ridhima\satellite-anomaly-detector"
.\venv\Scripts\Activate.ps1
cd simulator
python -m simulator.simulator
```

**Terminal 3 - Dashboard:**
```powershell
cd "C:\Users\hp\OneDrive\Desktop\spotted new\check\new\Spotted\ridhima\satellite-anomaly-detector"
.\venv\Scripts\Activate.ps1
cd dashboard
streamlit run streamlit_app.py --server.port 8501
```

**Linux/Mac/Git Bash:**

If you have bash available, you can use the provided script:
```bash
bash scripts/start_demo.sh
```

Or run in 3 separate terminals:

**Terminal 1 - Backend:**
```bash
export PYTHONPATH=$PWD
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 - Simulator:**
```bash
cd simulator
python -m simulator.simulator
```

**Terminal 3 - Dashboard:**
```bash
cd dashboard
streamlit run streamlit_app.py --server.port 8501
```

### Option B: Run Services Individually

You can also start services one at a time. Just make sure to start them in this order:
1. Backend first (needed by simulator and dashboard)
2. Simulator second (sends data to backend)
3. Dashboard last (reads from backend)

## 🌐 Step 6: Access the Services

Once all services are running:

- **Backend API:** Open http://127.0.0.1:8000 in your browser
- **API Documentation:** Open http://127.0.0.1:8000/docs (Swagger UI)
- **Dashboard:** Open http://localhost:8501 in your browser

The dashboard will automatically connect to the backend and start displaying:
- Real-time anomaly detection
- Telemetry data visualization
- Alert cards
- Health panels
- Orbit visualizations

## 📊 What to Expect

1. **Backend Terminal:** You'll see logs showing incoming telemetry data and anomaly detections
2. **Simulator Terminal:** You'll see messages like "Sending telemetry for SAT-1", "SAT-2", etc.
3. **Dashboard Browser:** The Streamlit dashboard will refresh every few seconds showing live data

## ⚠️ Troubleshooting

### Port Already in Use

If you get an error like `Address already in use`:
- Check if ports 8000 or 8501 are already in use
- Stop the processes using those ports or change the ports in the commands

**Windows - Find process using port:**
```powershell
netstat -ano | findstr :8000
```

### Import Errors

If you get import errors like `ModuleNotFoundError`:
- Make sure you're in the correct directory
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Database Errors

The SQLite database (`satellite_demo.db`) will be created automatically in the project root. If you encounter database errors:
- Delete `satellite_demo.db` and restart the backend
- Check file permissions

### TensorFlow Issues

If TensorFlow installation fails:
- Ensure you have Python 3.8-3.11 (TensorFlow 2.x supports these)
- On Windows, you may need Microsoft Visual C++ Redistributable
- Try: `pip install tensorflow --upgrade`

## 🛑 Stopping the Services

To stop all services:
- Press `Ctrl+C` in each terminal window
- Or close the terminal windows

## 📝 Quick Reference Commands

**Windows Users - Easiest Method:**
Just double-click these batch files in the `scripts` folder:
- `scripts\start_backend.bat`
- `scripts\start_simulator.bat`
- `scripts\start_dashboard.bat`

**Activate Virtual Environment:**
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

**Start Backend:**
```bash
# Windows PowerShell (from project root)
$env:PYTHONPATH = $PWD
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload

# Linux/Mac (from project root)
export PYTHONPATH=$PWD
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload
```

**Start Simulator:**
```bash
cd simulator
python -m simulator.simulator
```

**Start Dashboard:**
```bash
cd dashboard
streamlit run streamlit_app.py --server.port 8501
```

## 🎉 You're All Set!

Once all three services are running, open your browser to http://localhost:8501 to see the live anomaly detection dashboard!

---

**Need Help?** Check the main README.md for more architectural details and system overview.
