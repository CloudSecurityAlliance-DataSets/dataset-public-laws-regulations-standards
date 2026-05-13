"""
Configuration management for CWE AI Analysis.

This module provides configuration handling via environment variables and .env files.
Configuration is centralized here to:
1. Keep hardcoded values out of the codebase
2. Allow different settings for development, testing, production
3. Make it easy to adjust paths and settings without code changes

Why Pydantic Settings:
    Pydantic's BaseSettings provides automatic environment variable loading,
    type coercion, and validation. This means we get clear error messages if
    configuration is invalid, rather than cryptic failures later.

Usage:
    # Get the singleton config instance
    from cwe_ai_analysis.config import get_config
    config = get_config()
    print(config.data_dir)

    # Or create a custom config
    from cwe_ai_analysis.config import Config
    config = Config(data_dir="/custom/path")
"""

import logging
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Application configuration loaded from environment variables.

    All settings can be overridden via environment variables with the CWE_AI_ prefix.
    For example, CWE_AI_DATA_DIR=/path/to/data

    Why These Defaults:
        - data_dir defaults to parent directory (../) because the scripts/ folder
          is inside the CWE directory which contains the CSV files
        - output_dir defaults to ./output to keep generated files separate
        - log_level defaults to INFO for production; use DEBUG for development
    """

    model_config = SettingsConfigDict(
        env_prefix="CWE_AI_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra environment variables
    )

    # Data directory containing CWE CSV/JSON files
    # Why Path type: Provides cross-platform path handling and useful methods
    data_dir: Path = Field(
        default=Path(".."),
        description="Directory containing CWE data files (CSV, JSON)",
    )

    # Output directory for generated files
    output_dir: Path = Field(
        default=Path("./output"),
        description="Directory for output files",
    )

    # Logging level
    # Why string instead of int: More readable in environment variables
    log_level: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
    )

    # Checkpoint file for resuming interrupted classification runs
    # Why Optional: Not needed for small runs, but essential for full classification
    checkpoint_file: Optional[Path] = Field(
        default=None,
        description="Path to checkpoint file for resuming interrupted runs",
    )

    # Batch size for checkpointing
    # Why 50: Balances between frequent saves (overhead) and losing progress
    checkpoint_batch_size: int = Field(
        default=50,
        ge=1,
        description="Number of entries to process before saving checkpoint",
    )

    # CWE data file names
    # Why configurable: Allows using different versions or custom extracts
    research_concepts_file: str = Field(
        default="CWE-Research-Concepts-1000.csv",
        description="Filename for Research Concepts view (CWE-1000)",
    )
    software_development_file: str = Field(
        default="CWE-Software-Development-699.csv",
        description="Filename for Software Development view (CWE-699)",
    )
    hardware_design_file: str = Field(
        default="CWE-Hardware-Design-1194.csv",
        description="Filename for Hardware Design view (CWE-1194)",
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """
        Validate that log_level is a valid Python logging level.

        Why this validator: Catch typos early with a clear error message,
        rather than silently falling back to a default or crashing later.
        """
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}, got '{v}'")
        return v_upper

    @field_validator("data_dir", "output_dir")
    @classmethod
    def resolve_path(cls, v: Path) -> Path:
        """
        Resolve paths to absolute paths.

        Why resolve: Relative paths can be confusing when the working directory
        changes. Absolute paths are unambiguous.
        """
        return v.resolve()

    def get_data_file_path(self, filename: str) -> Path:
        """
        Get the full path to a data file.

        Why this method: Centralizes path construction, making it easier to
        change the data directory structure later if needed.
        """
        return self.data_dir / filename

    def get_output_file_path(self, filename: str) -> Path:
        """
        Get the full path for an output file, creating the directory if needed.

        Why create directory: Avoids "directory not found" errors when writing
        output files. Users shouldn't need to manually create directories.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir / filename

    def setup_logging(self) -> None:
        """
        Configure logging based on settings.

        Why centralized: Ensures consistent logging format across all modules.
        The format includes timestamp and module name for debugging.
        """
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


@lru_cache(maxsize=1)
def get_config() -> Config:
    """
    Get the singleton configuration instance.

    Why singleton pattern (via lru_cache):
        - Configuration should be consistent across the application
        - Avoid re-parsing environment variables repeatedly
        - The cache can be cleared with get_config.cache_clear() for testing

    Returns:
        Config: The application configuration instance.
    """
    return Config()
