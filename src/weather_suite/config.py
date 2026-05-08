"""Runtime configuration for the weather analytics suite."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    api_key: str
    db_path: Path
    request_timeout_seconds: int = 12
    default_city: str = "Mumbai"
    anomaly_z_threshold: float = 2.2
    rolling_window: int = 8


def load_settings() -> Settings:
    """Load settings from .env without leaking secrets into source control."""

    load_dotenv(PROJECT_ROOT / ".env")
    load_dotenv(PROJECT_ROOT / ".env.example")

    api_key = os.getenv("WEATHER_API_KEY") or os.getenv("OPENWEATHER_API_KEY") or ""
    db_path = Path(os.getenv("WEATHER_DB_PATH", PROJECT_ROOT / "data" / "weather_warehouse.duckdb"))

    return Settings(
        api_key=api_key.strip().strip("'").strip('"'),
        db_path=db_path,
        request_timeout_seconds=int(os.getenv("WEATHER_TIMEOUT_SECONDS", "12")),
        default_city=os.getenv("DEFAULT_CITY", "Mumbai"),
        anomaly_z_threshold=float(os.getenv("ANOMALY_Z_THRESHOLD", "2.2")),
        rolling_window=int(os.getenv("ANOMALY_ROLLING_WINDOW", "8")),
    )
