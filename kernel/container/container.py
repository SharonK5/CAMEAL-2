# kernel/container/container.py
from typing import Any, Callable, List, Optional, Tuple, Type, TypeVar, Union
from contextlib import contextmanager

from .cache import Cache
from .dependency import Dependency
from .exceptions import StateError
from .registry import Registry
from .registration import Registration
from .resolver import Resolver
from .scopes import Scope
from .state import ContainerState
from .validator import Validator
from ..lifecycle import Lifecycle, HealthStatus

T = TypeVar('T')


class Container(Lifecycle):
    def __init__(self) -> None:
        super().__init__()
        self._registry = Registry()
        self._cache = Cache()
        self._validator = Validator(self._registry)
        self._resolver = Resolver(self._registry, self._cache, self._validator)
        self._registration = Registration(self._registry)
        self._request_id: Optional[str] = None
        self._container_state = ContainerState.CREATED

    # ------------------------------------------------------------------
    # Lifecycle Implementation
    # ------------------------------------------------------------------

    def discover(self) -> None:
        self._transition(ContainerState.CREATED, ContainerState.DISCOVERED)
        super().discover()

    def validate(self) -> None:
        self._transition(ContainerState.DISCOVERED, ContainerState.VALIDATED)
        self._validator.validate_graph()
        super().validate()

    def initialize(self) -> None:
        self._transition(ContainerState.VALIDATED, ContainerState.INITIALIZED)
        super().initialize()

    def boot(self) -> None:
        self._transition(ContainerState.INITIALIZED, ContainerState.FROZEN)
        self.freeze()
        super().start()

    def start(self) -> None:
        self._transition(ContainerState.FROZEN, ContainerState.RUNNING)
        super().start()

    def stop(self) -> None:
        self._transition(ContainerState.RUNNING, ContainerState.STOPPED)
        super().stop()

    def dispose(self) -> None:
        self._transition(ContainerState.STOPPED, ContainerState.DISPOSED)
        super().dispose()

    def health(self) -> HealthStatus:
        if self._container_state in (ContainerState.FAILED, ContainerState.DISPOSED):
            return HealthStatus.UNHEALTHY
        if self._container_state == ContainerState.RUNNING:
            return HealthStatus.HEALTHY
        return HealthStatus.DEGRADED

    def _transition(self, from_state: ContainerState, to_state: ContainerState) -> None:
        if self._container_state != from_state:
            raise StateError(f"Cannot transition from {self._container_state} to {to_state}")
        self._container_state = to_state

    # ------------------------------------------------------------------
    # Registration API
    # ------------------------------------------------------------------

    def register(
        self,
        interface: Type[T],
        implementation: Union[Type[T], Callable[[], T]],
        scope: Scope = Scope.TRANSIENT,
        name: Optional[str] = None,
        tags: Tuple[str, ...] = (),
        is_factory: bool = False,
        lazy: bool = False,
    ) -> None:
        if self._container_state not in (ContainerState.CREATED, ContainerState.DISCOVERED):
            raise StateError(f"Cannot register after state {self._container_state}")
        self._registration.register(interface, implementation, scope, name, tags, is_factory, lazy)

    def register_singleton(self, interface: Type[T], instance: T, name: Optional[str] = None, tags: Tuple[str, ...] = ()) -> None:
        self.register(interface, lambda: instance, Scope.SINGLETON, name, tags)

    # ------------------------------------------------------------------
    # Resolution API
    # ------------------------------------------------------------------

    def resolve(self, interface: Type[T]) -> T:
        return self._resolver.resolve(interface, self._request_id)

    def resolve_by_name(self, interface: Type[T], name: str) -> T:
        return self._resolver.resolve_by_name(interface, name, self._request_id)

    def resolve_by_tag(self, tag: str) -> List[Any]:
        return self._resolver.resolve_by_tag(tag, self._request_id)

    def contains(self, interface: Type) -> bool:
        return self._registry.has_interface(interface)

    # ------------------------------------------------------------------
    # Request Scope API
    # ------------------------------------------------------------------

    def begin_request(self, request_id: str) -> None:
        self._request_id = request_id
        if not self._cache.has_request(request_id):
            self._cache.set_request_cache(request_id)

    def end_request(self, request_id: str) -> None:
        if self._request_id == request_id:
            self._request_id = None
        self._cache.clear_request(request_id)

    @contextmanager
    def request_scope(self, request_id: str):
        self.begin_request(request_id)
        try:
            yield
        finally:
            self.end_request(request_id)

    # ------------------------------------------------------------------
    # Validation & Freezing
    # ------------------------------------------------------------------

    def freeze(self) -> None:
        self._registry.freeze()

    def is_frozen(self) -> bool:
        return self._registry.is_frozen()

    def clear(self) -> None:
        self._cache.clear_all()

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def statistics(self) -> dict:
        stats = self._registry.statistics()
        stats.update(self._cache.statistics())
        stats["state"] = self._container_state.value
        stats["request_id"] = self._request_id
        return stats

    # ------------------------------------------------------------------
    # Internal Properties
    # ------------------------------------------------------------------

    @property
    def registry(self) -> Registry:
        return self._registry

    @property
    def cache(self) -> Cache:
        return self._cache

    @property
    def resolver(self) -> Resolver:
        return self._resolver

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        frozen = " (frozen)" if self.is_frozen() else ""
        return f"Container(registrations={len(self._registry.list())}{frozen})"
