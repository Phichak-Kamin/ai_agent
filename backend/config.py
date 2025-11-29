from __future__ import annotations
from pathlib import Path
from typing import Final
from pydantic_settings import BaseSettings

BASE_DIR: Final[Path] = Path(__file__).resolve().parent


class DataPaths:
    root: Path = BASE_DIR / "data"
    schedule: Path = root / "schedule.json"
    processing_time: Path = root / "processing_time.json"
    materials_usage: Path = root / "materials_usage.json"
    materials_available: Path = root / "materials_available.json"
    machines: Path = root / "machines.json"


class Settings(BaseSettings):
    factory_name: str = "Blue River Smart Factory"
    llm_model: str = "gpt-4o-mini"

    openai_api_key: str | None = None
    openai_base_url: str | None = None

    data_paths: DataPaths = DataPaths()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
