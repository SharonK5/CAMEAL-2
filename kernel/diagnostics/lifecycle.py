# kernel/diagnostics/lifecycle.py
from .diagnostics import Diagnostics
from ..lifecycle import Lifecycle, HealthStatus


class DiagnosticsLifecycle(Lifecycle):
    def __init__(self, diagnostics: Diagnostics):
        super().__init__()
        self._diagnostics = diagnostics

    def start(self) -> None:
        self._diagnostics.start()

    def stop(self) -> None:
        self._diagnostics.stop()

    def health(self) -> HealthStatus:
        return HealthStatus.HEALTHY if self._diagnostics.running else HealthStatus.UNHEALTHY

    def _on_health(self) -> bool:
        return self.health() == HealthStatus.HEALTHY
