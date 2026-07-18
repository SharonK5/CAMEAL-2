# kernel/container/registration.py
from typing import Any, Callable, Optional, Tuple, Type, Union

from .dependency import Dependency
from .registry import Registry
from .scopes import Scope


class Registration:
    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    def register(
        self,
        interface: Type,
        implementation: Union[Type, Callable[[], Any]],
        scope: Scope = Scope.TRANSIENT,
        name: Optional[str] = None,
        tags: Tuple[str, ...] = (),
        is_factory: bool = False,
        lazy: bool = False,
    ) -> None:
        dep = Dependency(interface, implementation, scope, name, tags, is_factory, lazy)
        self._registry.register(dep)

    def singleton(self, interface: Type, implementation: Union[Type, Callable[[], Any]], name: Optional[str] = None, tags: Tuple[str, ...] = ()) -> None:
        self.register(interface, implementation, Scope.SINGLETON, name, tags)

    def request(self, interface: Type, implementation: Union[Type, Callable[[], Any]], name: Optional[str] = None, tags: Tuple[str, ...] = ()) -> None:
        self.register(interface, implementation, Scope.REQUEST, name, tags)

    def transient(self, interface: Type, implementation: Union[Type, Callable[[], Any]], name: Optional[str] = None, tags: Tuple[str, ...] = ()) -> None:
        self.register(interface, implementation, Scope.TRANSIENT, name, tags)

    def factory(self, interface: Type, factory: Callable[[], Any], name: Optional[str] = None, tags: Tuple[str, ...] = ()) -> None:
        self.register(interface, factory, Scope.TRANSIENT, name, tags, is_factory=True)
