# security/services/service_registration.py
from __future__ import annotations

import re
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Tuple, Type

from .base.exceptions import ServiceValidationError
from .base.service import Service


# SemVer pattern: MAJOR.MINOR.PATCH
_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True, slots=True)
class ServiceRegistration:
    """
    Immutable service registration metadata.

    Attributes:
        name: Unique service name (will be normalized to lower-case, stripped).
        service_type: Concrete Service subclass.
        domain: Security domain (will be normalized to lower-case, stripped).
        version: Semantic version (MAJOR.MINOR.PATCH).
        dependencies: Tuple of service names this service depends on (will be normalized).
        configuration: Immutable configuration mapping.
        tags: Tuple of tags for grouping (will be normalized to stripped lower-case).
        singleton: Whether the service should be a singleton (cached).
        enabled: Whether the service is active (can be toggled without unregistering).
    """

    name: str
    service_type: Type[Service]
    domain: str
    version: str = "1.0.0"

    dependencies: Tuple[str, ...] = ()

    configuration: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    tags: Tuple[str, ...] = ()

    singleton: bool = True
    enabled: bool = True

    def __post_init__(self) -> None:
        # 1. Validate service_type is a class and a subclass of Service
        if not isinstance(self.service_type, type):
            raise ServiceValidationError(
                "service_type must be a class."
            )
        if not issubclass(self.service_type, Service):
            raise ServiceValidationError(
                "service_type must inherit from Service."
            )

        # 2. Normalize name and domain
        norm_name = self.name.strip().lower()
        if not norm_name:
            raise ServiceValidationError("Service name cannot be empty.")
        object.__setattr__(self, "name", norm_name)

        norm_domain = self.domain.strip().lower()
        if not norm_domain:
            raise ServiceValidationError("Service domain cannot be empty.")
        object.__setattr__(self, "domain", norm_domain)

        # 3. Validate version (semantic)
        if not _VERSION_PATTERN.match(self.version):
            raise ServiceValidationError(
                "Version must follow semantic versioning (MAJOR.MINOR.PATCH)."
            )

        # 4. Validate and normalize dependencies
        deps = []
        seen = set()
        for dep in self.dependencies:
            if not isinstance(dep, str):
                raise ServiceValidationError("Dependencies must be strings.")
            dep_norm = dep.strip().lower()
            if not dep_norm:
                raise ServiceValidationError("Dependency names cannot be empty.")
            if dep_norm in seen:
                raise ServiceValidationError(
                    f"Duplicate dependency '{dep_norm}'."
                )
            seen.add(dep_norm)
            deps.append(dep_norm)
        object.__setattr__(self, "dependencies", tuple(deps))

        # 5. Validate and normalize tags
        tags_norm = []
        for tag in self.tags:
            if not isinstance(tag, str):
                raise ServiceValidationError("Tags must be strings.")
            tag_norm = tag.strip().lower()
            if not tag_norm:
                raise ServiceValidationError("Tags cannot be empty.")
            # allow duplicates? Probably not, but we don't enforce uniqueness.
            tags_norm.append(tag_norm)
        object.__setattr__(self, "tags", tuple(tags_norm))

        # 6. Ensure configuration is immutable
        object.__setattr__(
            self,
            "configuration",
            MappingProxyType(dict(self.configuration))
        )

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    @property
    def qualified_name(self) -> str:
        """Human‑oriented qualified name: domain.name:version."""
        return f"{self.domain}.{self.name}:{self.version}"

    @property
    def identifier(self) -> str:
        """Stable identifier for logs and auditing: domain:name:version."""
        return f"{self.domain}:{self.name}:{self.version}"

    def has_dependency(self, name: str) -> bool:
        """Check if a service name is in dependencies (case‑insensitive)."""
        return name.strip().lower() in self.dependencies

    def has_tag(self, tag: str) -> bool:
        """Check if a tag is present (case‑insensitive)."""
        return tag.strip().lower() in self.tags

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary (for serialisation/debugging)."""
        return {
            "name": self.name,
            "service_type": self.service_type.__name__,
            "domain": self.domain,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "configuration": dict(self.configuration),
            "tags": list(self.tags),
            "singleton": self.singleton,
            "enabled": self.enabled,
        }
