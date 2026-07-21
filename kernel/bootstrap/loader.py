# kernel/bootstrap/loader.py
"""
Loads manifests and modules.
"""

import importlib
from typing import Any, Dict, Optional, Type
from pathlib import Path

from .exceptions import LoaderError


class Loader:
    """
    Loads manifests and Python modules.
    """

    @staticmethod
    def load_manifest(path: str) -> Dict[str, Any]:
        """
        Load a plugin manifest file.
        """
        import yaml

        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise LoaderError(f"Failed to load manifest '{path}': {e}") from e

    @staticmethod
    def load_class(class_path: str) -> Type:
        """
        Load a class from a string path.

        Example: "my_package.MyClass"
        """
        try:
            module_name, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        except Exception as e:
            raise LoaderError(f"Failed to load class '{class_path}': {e}") from e

    @staticmethod
    def instantiate(class_path: str, *args, **kwargs) -> Any:
        """
        Instantiate a class from a string path.
        """
        cls = Loader.load_class(class_path)
        return cls(*args, **kwargs)
