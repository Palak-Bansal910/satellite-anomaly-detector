#!/bin/bash
cd "$(dirname "$0")/.."
# activate venv if you like:
# source venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
# to run without reload, use:
# uvicorn api.main:app --host
# to run with multiple workers, use:
# uvicorn api.main:app --host
