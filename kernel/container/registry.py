# kernel/container/registry.py
from typing import Any, Dict, List, Optional, Type

from .dependency import Dependency
from .exceptions import RegistrationError


class Registry:
    def __init__(self) -> None:
        self._dependencies: Dict[str, Dependency] = {}
        self._by_interface: Dict[Type, List[str]] = {}
        self._by_tag: Dict[str, List[str]] = {}
        self._frozen: bool = False

    def register(self, dependency: Dependency) -> None:
        if self._frozen:
            raise RegistrationError("Registry is frozen; cannot register new dependencies")
        key = dependency.identifier
        if key in self._dependencies:
            raise RegistrationError(f"Dependency '{key}' already registered")
        self._dependencies[key] = dependency
        self._by_interface.setdefault(dependency.interface, []).append(key)
        for tag in dependency.tags:
            self._by_tag.setdefault(tag, []).append(key)

    def get(self, identifier: str) -> Optional[Dependency]:
        return self._dependencies.get(identifier)

    def get_by_interface(self, interface: Type) -> List[Dependency]:
        keys = self._by_interface.get(interface, [])
        return [self._dependencies[k] for k in keys if k in self._dependencies]

    def get_by_tag(self, tag: str) -> List[Dependency]:
        keys = self._by_tag.get(tag, [])
        return [self._dependencies[k] for k in keys if k in self._dependencies]

    def has_interface(self, interface: Type) -> bool:
        return interface in self._by_interface

    def list(self) -> List[str]:
        return list(self._dependencies.keys())

    def freeze(self) -> None:
        self._frozen = True

    def is_frozen(self) -> bool:
        return self._frozen

    def clear(self) -> None:
        self._dependencies.clear()
        self._by_interface.clear()
        self._by_tag.clear()
        self._frozen = False

    def statistics(self) -> Dict[str, Any]:
        return {
            "registrations": len(self._dependencies),
            "interfaces": len(self._by_interface),
            "tags": len(self._by_tag),
            "frozen": self._frozen,
        }
