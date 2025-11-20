# -*- coding: utf-8 -*-
"""
Configuration settings - Similar a config/ de Laravel
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Application settings"""

    # App
    APP_NAME: str = os.getenv("APP_NAME", "ML Prediction Service")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "5000"))

    # Paths
    BASE_DIR: Path = BASE_DIR
    MODEL_PATH: str = os.getenv("MODEL_PATH", "storage/models/random_forest_model.pkl")
    DATASET_PATH: str = os.getenv("DATASET_PATH", "storage/datasets/synthetic_data.csv")

    # Geolocation - Centro Santa Cruz de la Sierra
    CENTRO_SCZ_LAT: float = float(os.getenv("CENTRO_SCZ_LAT", "-17.783889"))
    CENTRO_SCZ_LON: float = float(os.getenv("CENTRO_SCZ_LON", "-63.182222"))

    # Model Training
    RANDOM_STATE: int = int(os.getenv("RANDOM_STATE", "42"))
    N_ESTIMATORS: int = int(os.getenv("N_ESTIMATORS", "100"))
    MAX_DEPTH: int = int(os.getenv("MAX_DEPTH", "10"))
    MIN_SAMPLES_SPLIT: int = int(os.getenv("MIN_SAMPLES_SPLIT", "5"))
    TEST_SIZE: float = float(os.getenv("TEST_SIZE", "0.2"))

    @staticmethod
    def get_full_path(relative_path: str) -> Path:
        """Convierte ruta relativa a absoluta"""
        return Settings.BASE_DIR / relative_path


# Singleton instance
settings = Settings()
