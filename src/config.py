from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


@dataclass(frozen=True)
class CityConfig:
    name: str
    region: str
    country: str
    snapshot_date: str


@dataclass(frozen=True)
class PathConfig:
    raw_data: Path
    interim_data: Path
    processed_data: Path
    metadata: Path
    database: Path
    reports: Path


@dataclass(frozen=True)
class FileConfig:
    listings_detailed_raw: str
    calendar_detailed_raw: str
    reviews_detailed_raw: str
    listings_detailed_extracted: str
    calendar_detailed_extracted: str
    reviews_detailed_extracted: str
    listings_summary: str
    reviews_summary: str
    neighbourhoods: str
    neighbourhoods_geojson: str


@dataclass(frozen=True)
class PipelineConfig:
    fail_on_validation_error: bool
    save_parquet: bool
    log_level: str


@dataclass(frozen=True)
class AppConfig:
    project_name: str
    project_version: str
    city: CityConfig
    paths: PathConfig
    files: FileConfig
    pipeline: PipelineConfig

    def raw_file(self, file_key: str) -> Path:
        return self.paths.raw_data / getattr(self.files, file_key)

    def interim_file(self, file_key: str) -> Path:
        return self.paths.interim_data / getattr(self.files, file_key)


def _resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def load_config(config_path: Path | None = None) -> AppConfig:
    config_file = config_path or CONFIG_PATH

    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with config_file.open("r", encoding="utf-8") as file:
        raw_config: dict[str, Any] = yaml.safe_load(file)

    city = CityConfig(
        name=raw_config["city"]["name"],
        region=raw_config["city"]["region"],
        country=raw_config["city"]["country"],
        snapshot_date=raw_config["city"]["snapshot_date"],
    )

    paths = PathConfig(
        raw_data=_resolve_path(raw_config["paths"]["raw_data"]),
        interim_data=_resolve_path(raw_config["paths"]["interim_data"]),
        processed_data=_resolve_path(raw_config["paths"]["processed_data"]),
        metadata=_resolve_path(raw_config["paths"]["metadata"]),
        database=_resolve_path(raw_config["paths"]["database"]),
        reports=_resolve_path(raw_config["paths"]["reports"]),
    )

    files = FileConfig(
        listings_detailed_raw=raw_config["files"]["listings_detailed_raw"],
        calendar_detailed_raw=raw_config["files"]["calendar_detailed_raw"],
        reviews_detailed_raw=raw_config["files"]["reviews_detailed_raw"],
        listings_detailed_extracted=raw_config["files"]["listings_detailed_extracted"],
        calendar_detailed_extracted=raw_config["files"]["calendar_detailed_extracted"],
        reviews_detailed_extracted=raw_config["files"]["reviews_detailed_extracted"],
        listings_summary=raw_config["files"]["listings_summary"],
        reviews_summary=raw_config["files"]["reviews_summary"],
        neighbourhoods=raw_config["files"]["neighbourhoods"],
        neighbourhoods_geojson=raw_config["files"]["neighbourhoods_geojson"],
    )

    pipeline = PipelineConfig(
        fail_on_validation_error=raw_config["pipeline"]["fail_on_validation_error"],
        save_parquet=raw_config["pipeline"]["save_parquet"],
        log_level=raw_config["pipeline"]["log_level"],
    )

    return AppConfig(
        project_name=raw_config["project"]["name"],
        project_version=raw_config["project"]["version"],
        city=city,
        paths=paths,
        files=files,
        pipeline=pipeline,
    )