#!/bin/bash
cd "$(dirname "$0")/.."
# activate venv if you like:
# source venv/bin/activate
cd dashboard
streamlit run streamlit_app.py --server.port 8501
