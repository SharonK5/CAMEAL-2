# kernel/container/validator.py
import inspect
from typing import Set, Type, get_type_hints

from .dependency import Dependency
from .exceptions import CircularDependencyError, ValidationError
from .registry import Registry


class Validator:
    def __init__(self, registry: Registry) -> None:
        self._registry = registry
        self._visiting: Set[str] = set()
        self._visited: Set[str] = set()

    def validate_registration(self, dependency: Dependency) -> None:
        if not (isinstance(dependency.implementation, type) or callable(dependency.implementation)):
            raise ValidationError(
                f"Implementation for {dependency.interface} must be a class or callable"
            )

    def validate_graph(self) -> None:
        self._visiting.clear()
        self._visited.clear()
        for identifier in self._registry.list():
            dep = self._registry.get(identifier)
            if dep:
                self._validate_node(dep)

    def _validate_node(self, dep: Dependency) -> None:
        identifier = dep.identifier
        if identifier in self._visiting:
            raise CircularDependencyError(f"Circular dependency detected: {identifier}")
        if identifier in self._visited:
            return

        self._visiting.add(identifier)

        # Validate the implementation's constructor and its dependencies
        impl = dep.implementation
        if isinstance(impl, type) and not inspect.isabstract(impl):
            self._validate_concrete_class(impl)

        # Validate all other registrations for the same interface
        interface = dep.interface
        for d in self._registry.get_by_interface(interface):
            if d.identifier != identifier:
                self._validate_node(d)

        self._visiting.remove(identifier)
        self._visited.add(identifier)

    def _validate_concrete_class(self, cls: Type) -> None:
        try:
            sig = inspect.signature(cls.__init__)
        except (ValueError, TypeError):
            return

        params = sig.parameters
        hints = get_type_hints(cls.__init__)

        for name, param in params.items():
            if name == "self":
                continue
            param_type = hints.get(name, param.annotation)
            if param_type is inspect.Parameter.empty:
                continue
            if param.default is not inspect.Parameter.empty:
                continue

            # Check if the parameter type can be resolved (registered or concrete class)
            # If it's registered, we need to validate its dependency graph
            if not self._validate_param_type(param_type):
                raise ValidationError(
                    f"Cannot resolve parameter '{name}' of type {param_type} for {cls}"
                )

    def _validate_param_type(self, interface: Type) -> bool:
        # If interface is registered, validate its dependencies recursively
        if self._registry.has_interface(interface):
            for dep in self._registry.get_by_interface(interface):
                self._validate_node(dep)
            return True

        # If it's a concrete class (not abstract), we can construct it if its dependencies are resolvable
        if isinstance(interface, type) and not inspect.isabstract(interface):
            try:
                sig = inspect.signature(interface.__init__)
            except (ValueError, TypeError):
                return True
            params = sig.parameters
            hints = get_type_hints(interface.__init__)
            for name, param in params.items():
                if name == "self":
                    continue
                param_type = hints.get(name, param.annotation)
                if param_type is inspect.Parameter.empty:
                    continue
                if param.default is not inspect.Parameter.empty:
                    continue
                if not self._validate_param_type(param_type):
                    return False
            return True

        # Unknown type or abstract class: cannot resolve
        return False
