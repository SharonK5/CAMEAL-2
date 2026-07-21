# kernel/scheduler/lifecycle.py
from .scheduler import Scheduler
from kernel.lifecycle import Lifecycle, HealthStatus


class SchedulerLifecycle(Lifecycle):
    def __init__(self, scheduler: Scheduler):
        super().__init__()
        self._scheduler = scheduler

    def start(self) -> None:
        self._scheduler.start()

    def stop(self) -> None:
        self._scheduler.stop()

    def health(self) -> HealthStatus:
        return HealthStatus.HEALTHY if self._scheduler._running else HealthStatus.UNHEALTHY

    def _on_health(self) -> bool:
        return self.health() == HealthStatus.HEALTHY
