# kernel/lifecycle/manager.py
import logging
import threading
from typing import Dict, List, Optional, Set, Type
from .lifecycle import Lifecycle, Pausable
from .states import LifecycleState
from .health import HealthReport
from .observer import LifecycleObserver
from .exceptions import LifecycleError

logger = logging.getLogger(__name__)


class LifecycleManager:
    """
    Orchestrates lifecycle of all registered components.

    Components are started in registration order and stopped in reverse order.
    """

    def __init__(self) -> None:
        self._components: List[Lifecycle] = []
        self._observers: List[LifecycleObserver] = []
        self._lock = threading.RLock()

    def register(self, component: Lifecycle) -> None:
        with self._lock:
            if component in self._components:
                raise LifecycleError(f"Component already registered: {component}")
            self._components.append(component)

    def unregister(self, component: Lifecycle) -> None:
        with self._lock:
            if component in self._components:
                self._components.remove(component)

    def add_observer(self, observer: LifecycleObserver) -> None:
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def remove_observer(self, observer: LifecycleObserver) -> None:
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    # ------------------------------------------------------------------
    # Lifecycle orchestration
    # ------------------------------------------------------------------

    def initialize_all(self) -> None:
        for comp in self._components:
            try:
                comp.initialize()
                self._notify_initialized(comp)
            except Exception as e:
                comp.fail(e)
                self._notify_failed(comp, e)
                logger.error(f"Failed to initialize {comp}: {e}")
                raise

    def validate_all(self) -> None:
        for comp in self._components:
            try:
                comp.validate()
                self._notify_validated(comp)
            except Exception as e:
                comp.fail(e)
                self._notify_failed(comp, e)
                logger.error(f"Failed to validate {comp}: {e}")
                raise

    def boot_all(self) -> None:
        for comp in self._components:
            try:
                comp.boot()
                self._notify_booted(comp)
            except Exception as e:
                comp.fail(e)
                self._notify_failed(comp, e)
                logger.error(f"Failed to boot {comp}: {e}")
                raise

    def start_all(self) -> None:
        for comp in self._components:
            try:
                comp.start()
                self._notify_started(comp)
            except Exception as e:
                comp.fail(e)
                self._notify_failed(comp, e)
                logger.error(f"Failed to start {comp}: {e}")
                raise

    def pause_all(self) -> None:
        for comp in self._components:
            if isinstance(comp, Pausable):
                try:
                    comp.pause()
                except Exception as e:
                    logger.error(f"Failed to pause {comp}: {e}")

    def resume_all(self) -> None:
        for comp in self._components:
            if isinstance(comp, Pausable):
                try:
                    comp.resume()
                except Exception as e:
                    logger.error(f"Failed to resume {comp}: {e}")

    def stop_all(self) -> None:
        for comp in reversed(self._components):
            try:
                comp.stop()
                self._notify_stopped(comp)
            except Exception as e:
                logger.error(f"Failed to stop {comp}: {e}")

    def shutdown_all(self) -> None:
        for comp in reversed(self._components):
            try:
                comp.shutdown()
                self._notify_shutdown(comp)
            except Exception as e:
                logger.error(f"Failed to shutdown {comp}: {e}")

    def dispose_all(self) -> None:
        for comp in reversed(self._components):
            try:
                comp.dispose()
                self._notify_disposed(comp)
            except Exception as e:
                logger.error(f"Failed to dispose {comp}: {e}")

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def health_all(self) -> Dict[str, HealthReport]:
        reports = {}
        for comp in self._components:
            try:
                reports[comp.__class__.__name__] = comp.health_report()
            except Exception as e:
                logger.error(f"Failed to get health for {comp}: {e}")
        return reports

    def diagnostics_all(self) -> Dict[str, Dict]:
        diag = {}
        for comp in self._components:
            diag[comp.__class__.__name__] = {
                "state": comp.state.value,
                "health": comp.health().value,
                "component": comp.__class__.__name__,
                "registered": True,
            }
        return diag

    # ------------------------------------------------------------------
    # Observer notification
    # ------------------------------------------------------------------

    def _notify_initialized(self, comp: Lifecycle) -> None:
        for obs in self._observers:
            try:
                obs.on_initialized(comp)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    def _notify_validated(self, comp: Lifecycle) -> None:
        for obs in self._observers:
            try:
                obs.on_validated(comp)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    def _notify_booted(self, comp: Lifecycle) -> None:
        for obs in self._observers:
            try:
                obs.on_booted(comp)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    def _notify_started(self, comp: Lifecycle) -> None:
        for obs in self._observers:
            try:
                obs.on_started(comp)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    def _notify_stopped(self, comp: Lifecycle) -> None:
        for obs in self._observers:
            try:
                obs.on_stopped(comp)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    def _notify_shutdown(self, comp: Lifecycle) -> None:
        for obs in self._observers:
            try:
                obs.on_shutdown(comp)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    def _notify_disposed(self, comp: Lifecycle) -> None:
        for obs in self._observers:
            try:
                obs.on_disposed(comp)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    def _notify_failed(self, comp: Lifecycle, error: Exception) -> None:
        for obs in self._observers:
            try:
                obs.on_failed(comp, error)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    @property
    def components(self) -> List[Lifecycle]:
        with self._lock:
            return self._components.copy()
