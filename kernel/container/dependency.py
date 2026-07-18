# kernel/container/dependency.py
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Tuple, Type, Union

from .scopes import Scope


@dataclass(frozen=True)
class Dependency:
    interface: Type
    implementation: Union[Type, Callable[[], Any]]
    scope: Scope = Scope.TRANSIENT
    name: Optional[str] = None
    tags: Tuple[str, ...] = field(default_factory=tuple)
    is_factory: bool = False
    lazy: bool = False

    @property
    def implementation_type(self) -> Optional[Type]:
        if isinstance(self.implementation, type):
            return self.implementation
        return None

    @property
    def is_callable(self) -> bool:
        return callable(self.implementation) and not isinstance(self.implementation, type)

    @property
    def identifier(self) -> str:
        base = self.interface.__name__
        if self.name:
            return f"{base}:{self.name}"
        return base

    def __repr__(self) -> str:
        return (
            f"Dependency(interface={self.interface.__name__}, "
            f"name={self.name!r}, scope={self.scope.value})"
        )
