# config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = f"sqlite:///{BASE_DIR}/pharmacy_erp.db"

DEBUG = True
