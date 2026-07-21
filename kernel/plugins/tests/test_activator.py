# kernel/plugins/tests/test_activator.py
import pytest
from unittest.mock import Mock

from kernel.plugins.activator import PluginActivator
from kernel.plugins.base.plugin import Plugin
from kernel.plugins.exceptions import PluginRegistrationError
from kernel.providers import ProviderRegistry
from kernel.managers import EngineManager, WorkflowManager, SchedulerManager
from kernel.lifecycle import HealthStatus


class DummyPlugin(Plugin):
    name = "dummy"
    version = "0.1.0"

    def register(self, provider_registry, engine_manager, workflow_manager, scheduler_manager):
        provider_registry.register("dummy_provider", Mock())
        engine_manager.register("dummy_engine", Mock(), [])
        workflow_manager.register("dummy_workflow", Mock())
        # ✅ Correct signature with keyword arguments
        scheduler_manager.register(target=lambda: None, interval=60, name="dummy_scheduler")

    def start(self): pass
    def stop(self): pass
    def health(self): return HealthStatus.HEALTHY
    def _on_health(self) -> bool: return True


class TestPluginActivator:
    @pytest.fixture
    def activator(self):
        return PluginActivator(
            provider_registry=ProviderRegistry(),
            engine_manager=EngineManager(),
            workflow_manager=WorkflowManager(),
            scheduler_manager=SchedulerManager(),
        )

    def test_activate_success(self, activator):
        plugin = DummyPlugin()
        activator.activate(plugin)

        assert activator._provider_registry.has("dummy_provider") is True
        assert activator._engine_manager.has("dummy_engine") is True
        assert activator._workflow_manager.has("dummy_workflow") is True

    def test_activate_failure(self, activator):
        class FailingPlugin(Plugin):
            name = "failing"
            version = "0.1.0"
            def register(self, *args, **kwargs):
                raise RuntimeError("registration failed")
            def start(self): pass
            def stop(self): pass
            def health(self): pass
            def _on_health(self) -> bool: return True

        plugin = FailingPlugin()
        with pytest.raises(PluginRegistrationError):
            activator.activate(plugin)

    def test_activate_with_existing_name(self, activator):
        plugin = DummyPlugin()
        activator.activate(plugin)
        with pytest.raises(PluginRegistrationError):
            activator.activate(plugin)
