# kernel/lifecycle/tests/test_observer.py
import pytest
from ..observer import LifecycleObserver, NullObserver
from ..manager import LifecycleManager
from ..health import HealthReport
from .conftest import DummyComponent


class DummyObserver(LifecycleObserver):
    def __init__(self):
        self.initialized = False
        self.validated = False
        self.booted = False
        self.started = False
        self.stopped = False
        self.shutdown = False
        self.disposed = False
        self.failed = False
        self.failed_error = None

    def on_initialized(self, component):
        self.initialized = True

    def on_validated(self, component):
        self.validated = True

    def on_booted(self, component):
        self.booted = True

    def on_started(self, component):
        self.started = True

    def on_stopped(self, component):
        self.stopped = True

    def on_shutdown(self, component):
        self.shutdown = True

    def on_disposed(self, component):
        self.disposed = True

    def on_failed(self, component, error):
        self.failed = True
        self.failed_error = error

    def on_health_changed(self, component, report):
        # Not needed for these tests
        pass


class TestObserverPattern:
    def test_observer_notifications(self):
        manager = LifecycleManager()
        observer = DummyObserver()
        comp = DummyComponent()

        manager.add_observer(observer)
        manager.register(comp)

        manager.initialize_all()
        assert observer.initialized is True

        manager.validate_all()
        assert observer.validated is True

        manager.boot_all()
        assert observer.booted is True

        manager.start_all()
        assert observer.started is True

        manager.stop_all()
        assert observer.stopped is True

        manager.shutdown_all()
        assert observer.shutdown is True

        manager.dispose_all()
        assert observer.disposed is True

    def test_observer_failure_notification(self):
        manager = LifecycleManager()
        observer = DummyObserver()
        comp = DummyComponent()
        comp.fail_on("initialize")

        manager.add_observer(observer)
        manager.register(comp)

        with pytest.raises(RuntimeError, match="Initialize failed"):
            manager.initialize_all()

        assert observer.failed is True
        assert "Initialize failed" in str(observer.failed_error)

    def test_null_observer(self):
        observer = NullObserver()
        comp = DummyComponent()
        observer.on_initialized(comp)
        observer.on_started(comp)
        observer.on_failed(comp, Exception("test"))
        # Should not raise
        assert True
