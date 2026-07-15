"""
===============================================================================
Module: context.context_registry

Governance Context Registry.

Stores and retrieves immutable GovernanceContext objects.

Security:
- Write operations (register, unregister, clear) are only available on the
  mutable registry. For runtime use, provide a ReadOnlyContextRegistry view.
===============================================================================
"""

from __future__ import annotations

import os
import stat
import warnings
from pathlib import Path
from typing import Dict, Tuple

from .context import GovernanceContext


class ContextRegistry:
    """
    In-memory mutable registry for GovernanceContext objects.
    """

    def __init__(self) -> None:
        self._contexts: Dict[str, GovernanceContext] = {}

    # -------------------------------------------------------------------------
    # Write operations (protected – use only during bootstrap)
    # -------------------------------------------------------------------------

    def register(self, identifier: str, context: GovernanceContext) -> None:
        """Register a GovernanceContext. Raises ValueError if identifier exists."""
        if identifier in self._contexts:
            raise ValueError(f"Context '{identifier}' already registered.")
        self._contexts[identifier] = context

    def unregister(self, identifier: str) -> None:
        """Remove a context. No-op if not found."""
        self._contexts.pop(identifier, None)

    def clear(self) -> None:
        """Remove all registered contexts."""
        self._contexts.clear()

    # -------------------------------------------------------------------------
    # Read operations (exposed via the read‑only wrapper)
    # -------------------------------------------------------------------------

    def get(self, identifier: str) -> GovernanceContext | None:
        return self._contexts.get(identifier)

    def contains(self, identifier: str) -> bool:
        return identifier in self._contexts

    def identifiers(self) -> tuple[str, ...]:
        return tuple(sorted(self._contexts.keys()))

    def contexts(self) -> tuple[GovernanceContext, ...]:
        return tuple(self._contexts.values())

    def __len__(self) -> int:
        return len(self._contexts)

    # -------------------------------------------------------------------------
    # Read‑only view factory
    # -------------------------------------------------------------------------

    def readonly(self) -> ReadOnlyContextRegistry:
        """
        Return a read‑only view of this registry.
        Use this for runtime services (e.g., ContextResolver).
        """
        return ReadOnlyContextRegistry(self)


class ReadOnlyContextRegistry:
    """
    Read‑only wrapper around a ContextRegistry.

    Exposes only read methods: get, contains, identifiers, contexts, __len__.
    Write methods (register, unregister, clear) are not available.
    """

    def __init__(self, registry: ContextRegistry) -> None:
        self._registry = registry

    def get(self, identifier: str) -> GovernanceContext | None:
        return self._registry.get(identifier)

    def contains(self, identifier: str) -> bool:
        return self._registry.contains(identifier)

    def identifiers(self) -> tuple[str, ...]:
        return self._registry.identifiers()

    def contexts(self) -> tuple[GovernanceContext, ...]:
        return self._registry.contexts()

    def __len__(self) -> int:
        return len(self._registry)


# -----------------------------------------------------------------------------
# InstitutionalRegistry (YAML loader) with filesystem permission check
# -----------------------------------------------------------------------------

import yaml
from .institutional import InstitutionalContext
from .exceptions import ContextNotFoundError, CircularParentError


class InstitutionalRegistry:
    """
    Immutable registry of institutional contexts loaded from YAML files.
    """

    def __init__(self, contexts: list[InstitutionalContext]):
        self._contexts: Dict[str, InstitutionalContext] = {
            ctx.identifier: ctx for ctx in contexts
        }
        self._validate_no_circular_parents()

    @classmethod
    def from_directory(cls, directory: Path) -> InstitutionalRegistry:
        """Load all *.yaml files from a directory, with a security check."""
        if not directory.exists():
            raise FileNotFoundError(f"Context directory not found: {directory}")

        # Security: warn if directory is world‑writable (Unix/Linux)
        if hasattr(os, 'stat'):
            mode = os.stat(directory).st_mode
            if mode & stat.S_IWOTH:
                warnings.warn(
                    f"Context directory '{directory}' is world‑writable. "
                    "This is a security risk. Consider `chmod 750`.",
                    SecurityWarning,
                    stacklevel=2,
                )

        contexts = []
        for yaml_file in sorted(directory.glob("*.yaml")):
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if not data:
                    raise ValueError(f"Empty or invalid YAML file: {yaml_file}")
                ctx = InstitutionalContext.from_dict(data)
                contexts.append(ctx)

        return cls(contexts)

    # ... (the rest: validation and query methods unchanged)
    # For brevity, I include only the changed method above.
    # The full class would keep get_parent, get_children, etc.
