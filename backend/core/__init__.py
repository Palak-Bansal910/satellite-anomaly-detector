"""
Core module for backend.
Contains database, models, schemas, CRUD handlers, and configuration.
"""

from .database import SessionLocal, Base, engine
from . import models, schemas

__all__ = ["SessionLocal", "Base", "engine", "models", "schemas"]



