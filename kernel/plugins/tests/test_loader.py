# kernel/plugins/tests/test_loader.py
import pytest
from unittest.mock import Mock, patch

from kernel.plugins.loader import PluginLoader
from kernel.plugins.registry import PluginRegistry
from kernel.plugins.manifest import PluginManifest
from kernel.plugins.base.plugin import Plugin
from kernel.plugins.exceptions import PluginLoadError   # ✅ added
from kernel.container import Container
from kernel.lifecycle import HealthStatus


class MockPlugin(Plugin):
    name = "test_plugin"
    version = "1.0.0"

    def register(self, provider_registry, engine_manager, workflow_manager, scheduler_manager):
        pass

    def start(self): pass
    def stop(self): pass
    def health(self): return HealthStatus.HEALTHY
    def _on_health(self) -> bool: return True


class TestPluginLoader:
    @pytest.fixture
    def container(self):
        return Container()

    @pytest.fixture
    def registry(self):
        return PluginRegistry()

    @pytest.fixture
    def loader(self, container, registry):
        return PluginLoader(container, registry)

    def test_load_success(self, loader, registry):
        manifest = PluginManifest(
            name="test_plugin",
            version="1.0.0",
            module="tests.test_plugin_module",
            providers=[],
            engines=[],
            workflows=[],
            schedulers=[],
        )
        with patch("importlib.import_module") as mock_import:
            mock_module = Mock()
            mock_module.TestPlugin = MockPlugin
            mock_import.return_value = mock_module

            plugin = loader.load(manifest)
            assert plugin.name == "test_plugin"
            assert plugin.version == "1.0.0"
            assert registry.get("test_plugin") is plugin

    def test_load_missing_module(self, loader):
        manifest = PluginManifest(
            name="missing",
            version="1.0.0",
            module="nonexistent.module",
            providers=[],
            engines=[],
            workflows=[],
            schedulers=[],
        )
        with patch("importlib.import_module", side_effect=ImportError):
            with pytest.raises(PluginLoadError):
                loader.load(manifest)

    def test_load_no_plugin_class(self, loader):
        manifest = PluginManifest(
            name="no_class",
            version="1.0.0",
            module="tests.no_class_module",
            providers=[],
            engines=[],
            workflows=[],
            schedulers=[],
        )
        # Patch _find_plugin_class to return None, simulating no plugin class found
        with patch.object(loader, '_find_plugin_class', return_value=None):
            with pytest.raises(PluginLoadError):
                loader.load(manifest)
