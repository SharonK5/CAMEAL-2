# kernel/lifecycle/lifecycle.py
import time
from abc import ABC, abstractmethod
from typing import Optional
from .states import LifecycleState
from .health import HealthStatus, HealthReport
from .transitions import is_valid_transition, is_valid_pause_transition
from .exceptions import LifecycleError


class Lifecycle(ABC):
    """
    Standard lifecycle for all kernel-managed components.

    Every component follows the same initialization, validation,
    boot, start, stop, shutdown, and dispose sequence.
    """

    def __init__(self) -> None:
        self._state = LifecycleState.CREATED
        self._start_time: Optional[float] = None
        self._version: Optional[str] = None

    @property
    def state(self) -> LifecycleState:
        return self._state

    @property
    def version(self) -> Optional[str]:
        return self._version

    def _transition(self, target: LifecycleState) -> None:
        if not is_valid_transition(self._state, target):
            raise LifecycleError(
                f"Invalid transition from {self._state} to {target}",
                current_state=self._state.value,
                target_state=target.value,
            )
        self._state = target

    def _pause_transition(self, target: LifecycleState) -> None:
        if not is_valid_pause_transition(self._state, target):
            raise LifecycleError(
                f"Invalid pause/resume transition from {self._state} to {target}",
                current_state=self._state.value,
                target_state=target.value,
            )
        self._state = target

    def initialize(self) -> None:
        self._transition(LifecycleState.INITIALIZED)
        self._on_initialize()

    def validate(self) -> None:
        self._transition(LifecycleState.VALIDATED)
        self._on_validate()

    def boot(self) -> None:
        self._transition(LifecycleState.BOOTED)
        self._on_boot()

    def start(self) -> None:
        self._transition(LifecycleState.STARTED)
        self._on_start()
        self._transition(LifecycleState.RUNNING)
        self._start_time = time.time()
        self._on_run()

    def stop(self) -> None:
        self._transition(LifecycleState.STOPPING)
        self._on_stop()
        self._transition(LifecycleState.STOPPED)

    def shutdown(self) -> None:
        self._transition(LifecycleState.SHUTDOWN)
        self._on_shutdown()

    def dispose(self) -> None:
        self._transition(LifecycleState.DISPOSED)
        self._on_dispose()

    def fail(self, error: Exception) -> None:
        self._state = LifecycleState.FAILED
        self._on_fail(error)

    def health(self) -> HealthStatus:
        return self._on_health()

    def health_report(self) -> HealthReport:
        uptime = time.time() - self._start_time if self._start_time else None
        status = self.health()
        healthy = status == HealthStatus.HEALTHY
        return HealthReport(
            component=self.__class__.__name__,
            state=self._state,
            healthy=healthy,
            uptime=uptime,
            version=self.version,
            message=("Operational" if healthy else f"Health: {status.value}"),
        )

    # ------------------------------------------------------------------
    # Template methods (overridable by subclasses)
    # ------------------------------------------------------------------

    def _on_initialize(self) -> None:
        pass

    def _on_validate(self) -> None:
        pass

    def _on_boot(self) -> None:
        pass

    def _on_start(self) -> None:
        pass

    def _on_run(self) -> None:
        pass

    def _on_stop(self) -> None:
        pass

    def _on_shutdown(self) -> None:
        pass

    def _on_dispose(self) -> None:
        pass

    def _on_fail(self, error: Exception) -> None:
        pass

    @abstractmethod
    def _on_health(self) -> HealthStatus:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(state={self._state})"


class Pausable(ABC):
    """
    Optional interface for components that support pausing and resuming.
    """

    @abstractmethod
    def pause(self) -> None:
        pass

    @abstractmethod
    def resume(self) -> None:
        pass
