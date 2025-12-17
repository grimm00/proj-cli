"""Configuration management with Pydantic and XDG compliance."""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


def get_xdg_config_home() -> Path:
    """Get XDG_CONFIG_HOME or default."""
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def get_xdg_data_home() -> Path:
    """Get XDG_DATA_HOME or default."""
    xdg_data = Path.home() / ".local" / "share"
    return Path(os.environ.get("XDG_DATA_HOME", xdg_data))


def get_config_dir() -> Path:
    """Get proj config directory."""
    return get_xdg_config_home() / "proj"


def get_data_dir() -> Path:
    """Get proj data directory."""
    return get_xdg_data_home() / "proj"


def get_config_file() -> Path:
    """Get config file path."""
    return get_config_dir() / "config.yaml"


class Config(BaseSettings):
    """Application configuration with environment variable support."""

    model_config = SettingsConfigDict(
        env_prefix="PROJ_",
        env_file=".env",
        extra="ignore",
    )

    # API Settings
    api_url: str = Field(
        default="http://localhost:5000",
        description="URL of the work-prod API",
    )

    # GitHub Settings
    github_token: Optional[str] = Field(
        default=None,
        description="GitHub personal access token",
    )
    github_username: Optional[str] = Field(
        default=None,
        description="GitHub username for scanning repos",
    )

    # Scan Settings
    local_scan_dirs: list[str] = Field(
        default_factory=lambda: [str(Path.home() / "Projects")],
        description="Directories to scan for local projects",
    )

    @classmethod
    def load(cls) -> "Config":
        """Load config from file and environment."""
        config_file = get_config_file()

        if config_file.exists():
            with open(config_file, encoding="utf-8") as f:
                file_config = yaml.safe_load(f) or {}
        else:
            file_config = {}

        # Environment variables override file config
        return cls(**file_config)

    def save(self) -> None:
        """Save current config to file."""
        config_dir = get_config_dir()
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = get_config_file()
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)


def ensure_dirs() -> None:
    """Ensure config and data directories exist."""
    get_config_dir().mkdir(parents=True, exist_ok=True)
    get_data_dir().mkdir(parents=True, exist_ok=True)
