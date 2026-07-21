# kernel/plugins/loader.py
"""
Plugin loader – loads plugins from manifests and modules.
"""

import importlib
import logging
from typing import Any, Optional, Type

from ..container import Container
from .manifest import PluginManifest
from .registry import PluginRegistry
from .exceptions import PluginLoadError
from .base.plugin import Plugin

logger = logging.getLogger(__name__)


class PluginLoader:
    """
    Loads a plugin from a manifest and returns an activated plugin instance.
    """

    def __init__(self, container: Container, plugin_registry: PluginRegistry) -> None:
        """
        Initialize the plugin loader.

        Args:
            container: The kernel container for dependency injection.
            plugin_registry: The registry to store loaded plugins.
        """
        self._container = container
        self._plugin_registry = plugin_registry

    def load(self, manifest: PluginManifest) -> Any:
        """
        Load a plugin from its manifest.

        Args:
            manifest: The plugin manifest.

        Returns:
            The loaded plugin instance.

        Raises:
            PluginLoadError: If the plugin cannot be loaded.
        """
        try:
            # Import the plugin module
            module = importlib.import_module(manifest.module)

            # Find the plugin class (look for a class with the same name as the module)
            plugin_class = self._find_plugin_class(module, manifest.name)

            if plugin_class is None:
                raise PluginLoadError(
                    f"No plugin class found in module '{manifest.module}'"
                )

            # Instantiate the plugin
            plugin_instance = self._instantiate_plugin(plugin_class)

            # Store in registry – pass manifest object
            self._plugin_registry.register(manifest, plugin_instance)

            logger.info(f"Loaded plugin: {manifest.name} v{manifest.version}")
            return plugin_instance

        except Exception as e:
            raise PluginLoadError(
                f"Failed to load plugin '{manifest.name}': {e}"
            ) from e

    def _find_plugin_class(self, module: Any, plugin_name: str) -> Optional[Type]:
        """
        Find the plugin class in the module.
        """
        # Look for a class with the same name as the plugin (capitalized)
        class_name = ''.join(word.capitalize() for word in plugin_name.split('_'))
        if hasattr(module, class_name):
            return getattr(module, class_name)

        # Look for any class that subclasses Lifecycle
        for attr_name in dir(module):
            if attr_name.startswith('_'):
                continue
            attr = getattr(module, attr_name)
            if isinstance(attr, type):
                # Check if it's a Lifecycle subclass
                if hasattr(attr, 'start') and hasattr(attr, 'stop'):
                    return attr

        return None

    def _instantiate_plugin(self, plugin_class: Type) -> Any:
        """
        Instantiate the plugin with dependency injection.
        """
        # Try to inject the container
        try:
            return plugin_class(container=self._container)
        except TypeError:
            # Try without arguments
            return plugin_class()
