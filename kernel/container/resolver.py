# kernel/container/resolver.py
import inspect
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Set, Type

from .cache import Cache
from .dependency import Dependency
from .exceptions import CircularDependencyError, ResolutionError
from .injector import Injector
from .registry import Registry
from .validator import Validator


class Resolver:
    def __init__(self, registry: Registry, cache: Cache, validator: Validator) -> None:
        self._registry = registry
        self._cache = cache
        self._validator = validator
        self._injector = Injector(self)
        self._resolving: Set[str] = set()
        self._request_id: Optional[str] = None

    def resolve(self, interface: Type, request_id: Optional[str] = None) -> Any:
        self._request_id = request_id
        identifier = interface.__name__

        # Check if interface is abstract (has abstract methods or is ABCMeta)
        if inspect.isabstract(interface):
            raise ResolutionError(f"Cannot instantiate abstract class: {interface}")

        return self._resolve_by_identifier(identifier, interface, request_id)

    def resolve_by_name(self, interface: Type, name: str, request_id: Optional[str] = None) -> Any:
        if inspect.isabstract(interface):
            raise ResolutionError(f"Cannot instantiate abstract class: {interface}")
        deps = self._registry.get_by_interface(interface)
        for dep in deps:
            if dep.name == name:
                return self._resolve_dep(dep, request_id)
        raise ResolutionError(f"No registration for {interface} with name '{name}'")

    def resolve_by_tag(self, tag: str, request_id: Optional[str] = None) -> List[Any]:
        deps = self._registry.get_by_tag(tag)
        return [self._resolve_dep(dep, request_id) for dep in deps]

    def _resolve_by_identifier(self, identifier: str, interface: Type, request_id: Optional[str] = None) -> Any:
        cached = self._cache.get(identifier, request_id)
        if cached is not None:
            return cached

        if identifier in self._resolving:
            raise CircularDependencyError(f"Circular dependency detected: {identifier}")

        deps = self._registry.get_by_interface(interface)
        if not deps:
            # If interface is a concrete class, try to construct it directly
            if isinstance(interface, type) and not inspect.isabstract(interface):
                self._resolving.add(identifier)
                try:
                    instance = self._injector.create(interface, request_id)
                finally:
                    self._resolving.remove(identifier)
                return instance
            raise ResolutionError(f"No registration for {interface}")

        dep = deps[0]
        return self._resolve_dep(dep, request_id)

    def _resolve_dep(self, dep: Dependency, request_id: Optional[str] = None) -> Any:
        identifier = dep.identifier
        cached = self._cache.get(identifier, request_id)
        if cached is not None:
            return cached

        if identifier in self._resolving:
            raise CircularDependencyError(f"Circular dependency detected: {identifier}")

        if dep.is_factory or dep.is_callable:
            instance = dep.implementation()
            self._cache.set(identifier, instance, dep.scope, request_id)
            return instance

        impl = dep.implementation
        if not isinstance(impl, type):
            raise ResolutionError(f"Implementation for {dep.interface} is not a class")

        if inspect.isabstract(impl):
            raise ResolutionError(f"Cannot instantiate abstract class: {impl}")

        self._resolving.add(identifier)
        try:
            instance = self._injector.create(impl, request_id)
        finally:
            self._resolving.remove(identifier)

        self._cache.set(identifier, instance, dep.scope, request_id)
        return instance

    def set_request_id(self, request_id: Optional[str]) -> None:
        self._request_id = request_id
