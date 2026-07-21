# kernel/bootstrap/tests/test_initializer.py
import pytest
from unittest.mock import Mock

from kernel.bootstrap.initializer import Initializer
from kernel.bootstrap.exceptions import InitializationError
from kernel.lifecycle import Lifecycle, HealthStatus


class DummyComponent(Lifecycle):
    def _on_health(self) -> HealthStatus:
        return HealthStatus.HEALTHY


class TestInitializer:
    def test_initialize(self):
        initializer = Initializer()
        container = Mock()
        engine_manager = DummyComponent()
        initializer.register_component("engine_manager", engine_manager)
        initializer.initialize(container)  # Should not raise

    def test_initialize_missing_component(self):
        initializer = Initializer()
        container = Mock()
        # No components registered; initialize should succeed (no‑op)
        initializer.initialize(container)  # Should not raise
        # If we want to test missing component, we could add a required flag later

    def test_initialize_component_failure(self):
        initializer = Initializer()

        class FailingComponent(DummyComponent):
            def initialize(self):
                raise ValueError("Initialization failed")

        container = Mock()
        engine_manager = FailingComponent()
        initializer.register_component("engine_manager", engine_manager)
        with pytest.raises(InitializationError, match="Initialization failed"):
            initializer.initialize(container)
