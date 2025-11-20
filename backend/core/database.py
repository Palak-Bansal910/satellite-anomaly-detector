from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pathlib import Path

# Use a local SQLite file for demo
BASE_DIR = Path(__file__).resolve().parents[2]  # project root
DB_PATH = BASE_DIR / "satellite_demo.db"
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DB_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
