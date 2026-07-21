# kernel/plugins/discovery.py
"""
Plugin discovery.
"""

import os
import glob
import yaml
from typing import List

from .manifest import PluginManifest
from .exceptions import PluginError   # ✅ corrected import


class PluginDiscovery:
    """
    Discovers plugins from directories.
    """

    @staticmethod
    def discover(directory: str) -> List[PluginManifest]:
        """
        Discover plugin manifests in a directory.

        Looks for files named 'manifest.yaml' or 'manifest.yml'.
        """
        manifests = []
        pattern = os.path.join(directory, "manifest.y*")
        for path in glob.glob(pattern):
            try:
                with open(path, 'r') as f:
                    data = yaml.safe_load(f)
                    manifest = PluginManifest.from_dict(data)
                    manifests.append(manifest)
            except Exception as e:
                raise PluginError(f"Failed to load manifest from {path}: {e}")
        return manifests
