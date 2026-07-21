# kernel/managers/plugin_manager.py
"""
Plugin Manager – manages plugin discovery and loading.
"""

from typing import Dict, List, Optional, Type, TYPE_CHECKING

from ..lifecycle import Lifecycle, HealthStatus
from ..container import Container
from .manager import Manager
from .exceptions import ManagerError

if TYPE_CHECKING:
    from ..plugins import PluginLoader, PluginRegistry, PluginDiscovery, PluginManifest


class PluginManager(Manager):
    def __init__(self, container: Container) -> None:
        super().__init__("plugin_manager")
        self._container = container
        # lazy import inside to avoid circularity
        from ..plugins import PluginRegistry, PluginLoader, PluginDiscovery
        self._plugin_registry = PluginRegistry()
        self._loader = PluginLoader(container, self._plugin_registry)
        self._discovery = PluginDiscovery()
        self._loaded_plugins: List[Lifecycle] = []

    def discover_and_load(self, directory: str) -> None:
        manifests = self._discovery.discover(directory)
        for manifest in manifests:
            plugin = self._loader.load(manifest)
            self._loaded_plugins.append(plugin)
            self.register(manifest.name, plugin)

    def start_all(self) -> None:
        for plugin in self._loaded_plugins:
            if plugin.state.value in ("created", "initialized", "validated"):
                plugin.start()

    def stop_all(self) -> None:
        for plugin in reversed(self._loaded_plugins):
            plugin.stop()

    def health_all(self) -> Dict[str, HealthStatus]:
        return {name: self._registry.get(name).health() for name in self._registry.list()}

    def __len__(self) -> int:
        return len(self._loaded_plugins)
