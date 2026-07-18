# kernel/lifecycle/tests/test_manager.py
import pytest
from ..manager import LifecycleManager
from ..states import LifecycleState
from ..exceptions import LifecycleError
from .conftest import DummyComponent, PausableDummyComponent


class TestLifecycleManager:
    def test_register(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        assert len(lifecycle_manager.components) == 1
        assert lifecycle_manager.components[0] == dummy_component

    def test_register_duplicate(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        with pytest.raises(LifecycleError, match="already registered"):
            lifecycle_manager.register(dummy_component)

    def test_unregister(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        lifecycle_manager.unregister(dummy_component)
        assert len(lifecycle_manager.components) == 0

    def test_initialize_all(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        lifecycle_manager.initialize_all()
        assert dummy_component.state == LifecycleState.INITIALIZED

    def test_initialize_all_failure(self, lifecycle_manager):
        comp = DummyComponent()
        comp.fail_on("initialize")
        lifecycle_manager.register(comp)
        with pytest.raises(RuntimeError, match="Initialize failed"):
            lifecycle_manager.initialize_all()
        assert comp.state == LifecycleState.FAILED

    def test_validate_all(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        lifecycle_manager.initialize_all()
        lifecycle_manager.validate_all()
        assert dummy_component.state == LifecycleState.VALIDATED

    def test_boot_all(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        lifecycle_manager.initialize_all()
        lifecycle_manager.validate_all()
        lifecycle_manager.boot_all()
        assert dummy_component.state == LifecycleState.BOOTED

    def test_start_all(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        lifecycle_manager.initialize_all()
        lifecycle_manager.validate_all()
        lifecycle_manager.boot_all()
        lifecycle_manager.start_all()
        assert dummy_component.state == LifecycleState.RUNNING

    def test_stop_all(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        lifecycle_manager.initialize_all()
        lifecycle_manager.validate_all()
        lifecycle_manager.boot_all()
        lifecycle_manager.start_all()
        lifecycle_manager.stop_all()
        assert dummy_component.state == LifecycleState.STOPPED

    def test_shutdown_all(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        lifecycle_manager.initialize_all()
        lifecycle_manager.validate_all()
        lifecycle_manager.boot_all()
        lifecycle_manager.start_all()
        lifecycle_manager.stop_all()
        lifecycle_manager.shutdown_all()
        assert dummy_component.state == LifecycleState.SHUTDOWN

    def test_dispose_all(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        lifecycle_manager.initialize_all()
        lifecycle_manager.validate_all()
        lifecycle_manager.boot_all()
        lifecycle_manager.start_all()
        lifecycle_manager.stop_all()
        lifecycle_manager.shutdown_all()
        lifecycle_manager.dispose_all()
        assert dummy_component.state == LifecycleState.DISPOSED

    def test_pause_all(self, lifecycle_manager):
        comp = PausableDummyComponent()
        lifecycle_manager.register(comp)
        lifecycle_manager.initialize_all()
        lifecycle_manager.validate_all()
        lifecycle_manager.boot_all()
        lifecycle_manager.start_all()
        lifecycle_manager.pause_all()
        assert comp._paused is True

    def test_resume_all(self, lifecycle_manager):
        comp = PausableDummyComponent()
        lifecycle_manager.register(comp)
        lifecycle_manager.initialize_all()
        lifecycle_manager.validate_all()
        lifecycle_manager.boot_all()
        lifecycle_manager.start_all()
        lifecycle_manager.pause_all()
        lifecycle_manager.resume_all()
        assert comp._paused is False

    def test_health_all(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        reports = lifecycle_manager.health_all()
        assert "DummyComponent" in reports
        assert reports["DummyComponent"].healthy is True

    def test_diagnostics_all(self, lifecycle_manager, dummy_component):
        lifecycle_manager.register(dummy_component)
        diag = lifecycle_manager.diagnostics_all()
        assert "DummyComponent" in diag
        assert diag["DummyComponent"]["state"] == "created"
