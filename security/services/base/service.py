# security/services/base/service.py
from __future__ import annotations

import time
import uuid
from abc import ABC, abstractmethod
from threading import RLock
from typing import Any, Dict, Optional

from .exceptions import ServiceLifecycleError
from .lifecycle import HealthStatus, Lifecycle, ServiceState


class BaseService(Lifecycle, ABC):
    """
    Core service abstraction with lifecycle, state machine, and metadata.
    Thread‑safe lifecycle transitions using an RLock.
    """

    # ------------------------------------------------------------------
    # Legal state transitions (centralised table)
    # ------------------------------------------------------------------
    LEGAL_TRANSITIONS = {
        ServiceState.CREATED:      {ServiceState.INITIALIZING},
        ServiceState.INITIALIZING: {ServiceState.INITIALIZED, ServiceState.FAILED},
        ServiceState.INITIALIZED:  {ServiceState.VALIDATING},
        ServiceState.VALIDATING:   {ServiceState.VALIDATED, ServiceState.FAILED},
        ServiceState.VALIDATED:    {ServiceState.STARTING, ServiceState.STOPPING},
        ServiceState.STARTING:     {ServiceState.RUNNING, ServiceState.FAILED},
        ServiceState.RUNNING:      {ServiceState.STOPPING, ServiceState.FAILED},
        ServiceState.STOPPING:     {ServiceState.STOPPED, ServiceState.FAILED},
        ServiceState.STOPPED:      {ServiceState.DISPOSED, ServiceState.STARTING},
        ServiceState.FAILED:       {ServiceState.DISPOSED},
        ServiceState.DISPOSED:     set(),
    }

    def __init__(self) -> None:
        self._state = ServiceState.CREATED
        self._lock = RLock()

        self._last_error: Optional[Exception] = None
        self._failed_at: Optional[float] = None

        self._created_at = time.time()
        self._initialized_at: Optional[float] = None
        self._validated_at: Optional[float] = None
        self._started_at: Optional[float] = None
        self._stopped_at: Optional[float] = None
        self._disposed_at: Optional[float] = None

        self._service_id = str(uuid.uuid4())

    # ------------------------------------------------------------------
    # Required metadata (abstract properties)
    # ------------------------------------------------------------------
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def version(self) -> str: ...

    @property
    @abstractmethod
    def security_domain(self) -> str: ...

    # ------------------------------------------------------------------
    # Public state & metadata
    # ------------------------------------------------------------------
    @property
    def state(self) -> ServiceState:
        with self._lock:
            return self._state

    @property
    def service_id(self) -> str:
        return self._service_id

    @property
    def last_error(self) -> Optional[Exception]:
        return self._last_error

    @property
    def failed_at(self) -> Optional[float]:
        return self._failed_at

    @property
    def created_at(self) -> float:
        return self._created_at

    @property
    def initialized_at(self) -> Optional[float]:
        return self._initialized_at

    @property
    def started_at(self) -> Optional[float]:
        return self._started_at

    @property
    def stopped_at(self) -> Optional[float]:
        return self._stopped_at

    @property
    def disposed_at(self) -> Optional[float]:
        return self._disposed_at

    @property
    def uptime(self) -> Optional[float]:
        if self._state == ServiceState.RUNNING and self._started_at:
            return time.time() - self._started_at
        return None

    # ------------------------------------------------------------------
    # Lifecycle implementation (thread‑safe)
    # ------------------------------------------------------------------
    def initialize(self) -> None:
        with self._lock:
            self._transition_to(ServiceState.INITIALIZING)
            try:
                self.before_initialize()
                self._on_initialize()
                self.after_initialize()
                self._initialized_at = time.time()
                self._transition_to(ServiceState.INITIALIZED)
                self._emit_event("initialized")
            except Exception as e:
                self._fail(e)

    def validate(self) -> None:
        with self._lock:
            self._transition_to(ServiceState.VALIDATING)
            try:
                self.before_validate()
                self._on_validate()
                self.after_validate()
                self._validated_at = time.time()
                self._transition_to(ServiceState.VALIDATED)
                self._emit_event("validated")
            except Exception as e:
                self._fail(e)

    def start(self) -> None:
        with self._lock:
            self._transition_to(ServiceState.STARTING)
            try:
                self.before_start()
                self._on_start()
                self.after_start()
                self._started_at = time.time()
                self._transition_to(ServiceState.RUNNING)
                self._emit_event("started")
            except Exception as e:
                self._fail(e)

    def shutdown(self) -> None:
        with self._lock:
            if self._state not in (ServiceState.RUNNING, ServiceState.VALIDATED, ServiceState.FAILED):
                if self._state == ServiceState.STOPPED:
                    return
                raise ServiceLifecycleError(
                    f"{self.name} cannot shutdown from {self._state.name}"
                )
            self._transition_to(ServiceState.STOPPING)
            try:
                self.before_shutdown()
                self._on_shutdown()
                self.after_shutdown()
                self._stopped_at = time.time()
                self._transition_to(ServiceState.STOPPED)
                self._emit_event("stopped")
            except Exception as e:
                self._fail(e)

    def dispose(self) -> None:
        with self._lock:
            if self._state not in (ServiceState.STOPPED, ServiceState.FAILED):
                raise ServiceLifecycleError(
                    f"{self.name} cannot dispose from {self._state.name}"
                )
            self._transition_to(ServiceState.DISPOSED)
            try:
                self.before_dispose()
                self._on_dispose()
                self.after_dispose()
                self._disposed_at = time.time()
                self._emit_event("disposed")
            except Exception as e:
                self._fail(e)

    def health(self) -> HealthStatus:
        with self._lock:
            if self._state == ServiceState.FAILED:
                return HealthStatus.UNHEALTHY
            if self._state == ServiceState.DISPOSED:
                return HealthStatus.UNHEALTHY
            if self._state != ServiceState.RUNNING:
                return HealthStatus.DEGRADED
            try:
                return self._on_health()
            except Exception:
                return HealthStatus.UNHEALTHY

    # ------------------------------------------------------------------
    # Centralised transition enforcement
    # ------------------------------------------------------------------
    def _transition_to(self, target: ServiceState) -> None:
        allowed = self.LEGAL_TRANSITIONS.get(self._state, set())
        if target not in allowed:
            raise ServiceLifecycleError(
                f"Illegal transition {self._state.name} -> {target.name} "
                f"for service {self.name}"
            )
        self._state = target

    def _fail(self, error: Exception) -> None:
        self._last_error = error
        self._failed_at = time.time()
        self._state = ServiceState.FAILED
        self._emit_event("failed", error=str(error))
        raise  # preserves original traceback

    # ------------------------------------------------------------------
    # Event hooks (optional, overridable)
    # ------------------------------------------------------------------
    def before_initialize(self) -> None: pass
    def after_initialize(self) -> None: pass
    def before_validate(self) -> None: pass
    def after_validate(self) -> None: pass
    def before_start(self) -> None: pass
    def after_start(self) -> None: pass
    def before_shutdown(self) -> None: pass
    def after_shutdown(self) -> None: pass
    def before_dispose(self) -> None: pass
    def after_dispose(self) -> None: pass

    # ------------------------------------------------------------------
    # Event emission (placeholder for monitoring)
    # ------------------------------------------------------------------
    def _emit_event(self, event_name: str, **kwargs) -> None:
        pass

    # ------------------------------------------------------------------
    # Template methods (mandatory)
    # ------------------------------------------------------------------
    @abstractmethod
    def _on_initialize(self) -> None: ...

    @abstractmethod
    def _on_validate(self) -> None: ...

    @abstractmethod
    def _on_start(self) -> None: ...

    @abstractmethod
    def _on_shutdown(self) -> None: ...

    @abstractmethod
    def _on_dispose(self) -> None: ...

    @abstractmethod
    def _on_health(self) -> HealthStatus: ...

    # ------------------------------------------------------------------
    # Metadata (extended)
    # ------------------------------------------------------------------
    def metadata(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "service_id": self._service_id,
                "name": self.name,
                "version": self.version,
                "security_domain": self.security_domain,
                "state": self.state.name,
                "created_at": self._created_at,
                "initialized_at": self._initialized_at,
                "validated_at": self._validated_at,
                "started_at": self._started_at,
                "stopped_at": self._stopped_at,
                "disposed_at": self._disposed_at,
                "uptime": self.uptime,
                "healthy": self.health() == HealthStatus.HEALTHY,
                "health_status": self.health().value,
                "last_error": str(self._last_error) if self._last_error else None,
                "failed_at": self._failed_at,
            }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"state={self.state.name}, "
            f"id={self._service_id[:8]})"
        )


# Alias for Service (expected by service layer)
Service = BaseService
