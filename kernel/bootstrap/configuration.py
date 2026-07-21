# kernel/bootstrap/configuration.py
"""
Configuration loader for the kernel bootstrap.
"""

import os
import json
import yaml
from typing import Any, Dict, Optional
from pathlib import Path

from .exceptions import ConfigurationError


class Configuration:
    """
    Loads and manages bootstrap configuration.
    """

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def load(self, source: Any) -> None:
        """
        Load configuration from a source.

        Supports:
            - dict: Direct dictionary.
            - str: File path (YAML or JSON).
            - Path: File path.
        """
        if isinstance(source, dict):
            self._data = source.copy()
        elif isinstance(source, (str, Path)):
            self._load_from_file(source)
        else:
            raise ConfigurationError(f"Unsupported configuration source: {type(source)}")

    def _load_from_file(self, path: str) -> None:
        """Load configuration from a file."""
        path = Path(path)
        if not path.exists():
            raise ConfigurationError(f"Configuration file not found: {path}")

        try:
            content = path.read_text()
            if path.suffix in (".yaml", ".yml"):
                data = yaml.safe_load(content)
            elif path.suffix == ".json":
                data = json.loads(content)
            else:
                raise ConfigurationError(f"Unsupported file type: {path.suffix}")
            self._data = data or {}
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}") from e

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        keys = key.split(".")
        value = self._data
        for k in keys:
            if not isinstance(value, dict):
                return default
            value = value.get(k)
            if value is None:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        keys = key.split(".")
        target = self._data
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        return self._data.copy()
