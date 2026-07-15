"""
===============================================================================
Module: context.yaml_context_provider

Loads GovernanceContext from YAML files (one per context).
===============================================================================
"""

from __future__ import annotations

import yaml
import warnings
from pathlib import Path
from typing import Sequence

from .context import GovernanceContext
from .context_builder import ContextBuilder
from .context_provider import ContextProvider
from .institutional import InstitutionalContext
from .jurisdictional import JurisdictionalContext
from .spatial import SpatialContext
from .temporal import TemporalContext
from .operational import OperationalContext


class YamlContextProvider(ContextProvider):
    """
    Reads GovernanceContext objects from YAML files.
    Each file must contain a dictionary with keys:
        institutional, jurisdictional, spatial, temporal, operational, metadata.
    The sub‑keys are passed directly to each respective context class.
    """

    def __init__(self, directory: Path) -> None:
        self._directory = directory
        self._contexts: dict[str, GovernanceContext] = {}
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return

        if not self._directory.exists():
            raise FileNotFoundError(f"Context directory not found: {self._directory}")

        for yaml_file in sorted(self._directory.glob("*.yaml")):
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if not data:
                    warnings.warn(f"Empty YAML file: {yaml_file}", UserWarning)
                    continue

                # Build each dimension from dicts
                institutional_data = data.get("institutional", {})
                jurisdictional_data = data.get("jurisdictional", {})
                spatial_data = data.get("spatial", {})
                temporal_data = data.get("temporal", {})
                operational_data = data.get("operational", {})
                metadata = data.get("metadata", {})

                # Note: InstitutionalContext requires 'identifier'
                inst = InstitutionalContext.from_dict(institutional_data)
                jur = JurisdictionalContext(**jurisdictional_data)
                spa = SpatialContext(**spatial_data)
                tmp = TemporalContext(**temporal_data)
                op = OperationalContext(**operational_data)

                # Build the full context
                builder = ContextBuilder()
                ctx = builder.build(
                    institutional=inst,
                    jurisdictional=jur,
                    spatial=spa,
                    temporal=tmp,
                    operational=op,
                    metadata=tuple(metadata.items()),  # tuple of pairs
                )

                # Use the institutional identifier as the primary key
                identifier = inst.identifier
                if identifier in self._contexts:
                    warnings.warn(f"Duplicate identifier '{identifier}' in {yaml_file}", UserWarning)
                self._contexts[identifier] = ctx

        self._loaded = True

    def get(self, identifier: str) -> GovernanceContext | None:
        self._load()
        return self._contexts.get(identifier)

    def list_identifiers(self) -> Sequence[str]:
        self._load()
        return tuple(self._contexts.keys())

    def load_all(self) -> Sequence[GovernanceContext]:
        self._load()
        return tuple(self._contexts.values())
