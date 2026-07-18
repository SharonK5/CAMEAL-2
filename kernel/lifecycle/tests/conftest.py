# kernel/lifecycle/tests/conftest.py
import pytest
from ..lifecycle import Lifecycle, Pausable
from ..manager import LifecycleManager
from ..states import LifecycleState
from ..health import HealthStatus, HealthReport


class DummyComponent(Lifecycle):
    def __init__(self, name: str = "Dummy"):
        super().__init__()
        self._name = name
        self._healthy = True
        self._fail_on = None

    def fail_on(self, method: str):
        self._fail_on = method

    def set_healthy(self, healthy: bool):
        self._healthy = healthy

    def _on_initialize(self) -> None:
        if self._fail_on == "initialize":
            raise RuntimeError("Initialize failed")

    def _on_validate(self) -> None:
        if self._fail_on == "validate":
            raise RuntimeError("Validate failed")

    def _on_boot(self) -> None:
        if self._fail_on == "boot":
            raise RuntimeError("Boot failed")

    def _on_start(self) -> None:
        if self._fail_on == "start":
            raise RuntimeError("Start failed")

    def _on_stop(self) -> None:
        if self._fail_on == "stop":
            raise RuntimeError("Stop failed")

    def _on_shutdown(self) -> None:
        if self._fail_on == "shutdown":
            raise RuntimeError("Shutdown failed")

    def _on_dispose(self) -> None:
        if self._fail_on == "dispose":
            raise RuntimeError("Dispose failed")

    def _on_health(self) -> HealthStatus:
        return HealthStatus.HEALTHY if self._healthy else HealthStatus.UNHEALTHY


class PausableDummyComponent(DummyComponent, Pausable):
    def __init__(self, name: str = "Pausable"):
        super().__init__(name)
        self._paused = False

    def pause(self) -> None:
        self._paused = True

    def resume(self) -> None:
        self._paused = False


@pytest.fixture
def dummy_component():
    return DummyComponent("TestComponent")


@pytest.fixture
def pausable_component():
    return PausableDummyComponent("TestPausable")


@pytest.fixture
def lifecycle_manager():
    return LifecycleManager()
