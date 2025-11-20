"""
Backend package initializer.
Makes 'core' and other backend modules discoverable.
"""

# Expose key modules for easier imports
from .core import database, models, schemas, crud
