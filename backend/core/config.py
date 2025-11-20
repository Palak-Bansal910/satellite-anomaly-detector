"""
Configuration helpers. Reads environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/telemetry")
NASA_DATA_FILE = os.getenv("NASA_DATA_FILE", "./data/nasa_telemetry.json")
