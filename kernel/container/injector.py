# kernel/container/injector.py
import inspect
from typing import Any, List, Optional, Type, get_type_hints

from .exceptions import ResolutionError


class Injector:
    def __init__(self, resolver: "Resolver") -> None:
        self._resolver = resolver

    def create(self, cls: Type, request_id: Optional[str] = None) -> Any:
        try:
            sig = inspect.signature(cls.__init__)
        except (ValueError, TypeError):
            return cls()

        params = sig.parameters
        hints = get_type_hints(cls.__init__)
        resolved_args: List[Any] = []

        for name, param in params.items():
            if name == "self":
                continue
            param_type = hints.get(name, param.annotation)
            if param_type is inspect.Parameter.empty:
                if param.default is not inspect.Parameter.empty:
                    resolved_args.append(param.default)
                continue

            if param.default is not inspect.Parameter.empty:
                try:
                    resolved = self._resolver.resolve(param_type, request_id)
                    resolved_args.append(resolved)
                except ResolutionError:
                    resolved_args.append(param.default)
            else:
                resolved = self._resolver.resolve(param_type, request_id)
                resolved_args.append(resolved)

        return cls(*resolved_args)
