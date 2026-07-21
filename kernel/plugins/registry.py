# kernel/plugins/registry.py
"""
Plugin registry – stores loaded plugins.
"""

from threading import RLock
from typing import Dict, List, Optional

from .manifest import PluginManifest
from .base.plugin import Plugin
from .exceptions import PluginNotFoundError, PluginRegistrationError


class PluginRegistry:
    """
    Registry for loaded plugins.
    """

    def __init__(self) -> None:
        self._plugins: Dict[str, Plugin] = {}
        self._manifests: Dict[str, PluginManifest] = {}
        self._lock = RLock()

    def register(self, manifest: PluginManifest, plugin: Plugin) -> None:
        """
        Register a plugin.

        Args:
            manifest: The plugin manifest.
            plugin: The loaded plugin instance.

        Raises:
            PluginRegistrationError: If a plugin with the same name is already registered.
        """
        with self._lock:
            if manifest.name in self._plugins:
                raise PluginRegistrationError(
                    f"Plugin '{manifest.name}' already registered"
                )
            self._plugins[manifest.name] = plugin
            self._manifests[manifest.name] = manifest

    def get(self, name: str) -> Plugin:
        """Retrieve a plugin by name."""
        with self._lock:
            if name not in self._plugins:
                raise PluginNotFoundError(f"Plugin '{name}' not found")
            return self._plugins[name]

    def get_manifest(self, name: str) -> PluginManifest:
        """Retrieve the manifest for a plugin by name."""
        with self._lock:
            if name not in self._manifests:
                raise PluginNotFoundError(f"Manifest for plugin '{name}' not found")
            return self._manifests[name]

    def has(self, name: str) -> bool:
        with self._lock:
            return name in self._plugins

    def list(self) -> List[str]:
        with self._lock:
            return list(self._plugins.keys())

    def __len__(self) -> int:
        with self._lock:
            return len(self._plugins)

    def __iter__(self):
        with self._lock:
            return iter(self._plugins.items())
