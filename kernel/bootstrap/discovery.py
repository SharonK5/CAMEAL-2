# kernel/bootstrap/discovery.py
"""
Plugin and package discovery.
"""

import os
import glob
import importlib
from typing import List, Optional
from pathlib import Path

from .exceptions import DiscoveryError


class Discovery:
    """
    Discovers plugins and packages.
    """

    @staticmethod
    def discover_plugins(directory: str) -> List[str]:
        """
        Discover plugin manifests in a directory.

        Returns:
            List of manifest file paths.
        """
        manifests = []
        pattern = os.path.join(directory, "manifest.y*")
        for path in glob.glob(pattern):
            manifests.append(path)
        return manifests

    @staticmethod
    def discover_packages(base_path: str) -> List[str]:
        """
        Discover Python packages in a directory.
        """
        packages = []
        for item in os.listdir(base_path):
            path = os.path.join(base_path, item)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, "__init__.py")):
                packages.append(item)
        return packages

    @staticmethod
    def load_module(module_path: str) -> Optional[object]:
        """
        Load a Python module dynamically.
        """
        try:
            return importlib.import_module(module_path)
        except Exception as e:
            raise DiscoveryError(f"Failed to load module '{module_path}': {e}") from e
