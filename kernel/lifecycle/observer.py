# kernel/lifecycle/observer.py
from abc import ABC, abstractmethod
from typing import Optional
from .lifecycle import Lifecycle
from .health import HealthReport


class LifecycleObserver(ABC):
    """
    Interface for observing lifecycle events.
    """

    @abstractmethod
    def on_initialized(self, component: Lifecycle) -> None:
        """Called after a component is initialized."""
        pass

    @abstractmethod
    def on_validated(self, component: Lifecycle) -> None:
        """Called after a component is validated."""
        pass

    @abstractmethod
    def on_booted(self, component: Lifecycle) -> None:
        """Called after a component is booted."""
        pass

    @abstractmethod
    def on_started(self, component: Lifecycle) -> None:
        """Called after a component is started."""
        pass

    @abstractmethod
    def on_stopped(self, component: Lifecycle) -> None:
        """Called after a component is stopped."""
        pass

    @abstractmethod
    def on_shutdown(self, component: Lifecycle) -> None:
        """Called after a component is shut down."""
        pass

    @abstractmethod
    def on_disposed(self, component: Lifecycle) -> None:
        """Called after a component is disposed."""
        pass

    @abstractmethod
    def on_failed(self, component: Lifecycle, error: Exception) -> None:
        """Called when a component fails."""
        pass

    @abstractmethod
    def on_health_changed(self, component: Lifecycle, report: HealthReport) -> None:
        """Called when a component's health changes."""
        pass


class NullObserver(LifecycleObserver):
    """No-op observer for convenience."""

    def on_initialized(self, component: Lifecycle) -> None:
        pass

    def on_validated(self, component: Lifecycle) -> None:
        pass

    def on_booted(self, component: Lifecycle) -> None:
        pass

    def on_started(self, component: Lifecycle) -> None:
        pass

    def on_stopped(self, component: Lifecycle) -> None:
        pass

    def on_shutdown(self, component: Lifecycle) -> None:
        pass

    def on_disposed(self, component: Lifecycle) -> None:
        pass

    def on_failed(self, component: Lifecycle, error: Exception) -> None:
        pass

    def on_health_changed(self, component: Lifecycle, report: HealthReport) -> None:
        pass
