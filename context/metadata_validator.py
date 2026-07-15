"""
===============================================================================
Module: context.metadata_validator

Validates metadata tuples against a schema to prevent spoofing and injection.
===============================================================================
"""

from __future__ import annotations

from typing import Any, Dict, Type, Optional, Set


class MetadataSchema:
    """
    Defines allowed keys, value types, and optional enumerated values.
    """

    def __init__(
        self,
        allowed_keys: Dict[str, Type],
        allowed_values: Optional[Dict[str, Set[Any]]] = None,
        required_keys: Optional[Set[str]] = None,
    ):
        self.allowed_keys = allowed_keys
        self.allowed_values = allowed_values or {}
        self.required_keys = required_keys or set()

    def validate(self, metadata: tuple[tuple[str, Any], ...]) -> None:
        """
        Raise ValueError if metadata violates the schema.
        """
        metadata_dict = dict(metadata)

        # Check required keys
        for key in self.required_keys:
            if key not in metadata_dict:
                raise ValueError(f"Missing required metadata key: '{key}'")

        # Check each key
        for key, value in metadata_dict.items():
            if key not in self.allowed_keys:
                raise ValueError(f"Unexpected metadata key: '{key}'")

            expected_type = self.allowed_keys[key]
            if not isinstance(value, expected_type):
                raise ValueError(
                    f"Metadata key '{key}' must be of type {expected_type.__name__}, got {type(value).__name__}"
                )

            if key in self.allowed_values and value not in self.allowed_values[key]:
                raise ValueError(
                    f"Metadata key '{key}' has invalid value '{value}'. Allowed: {self.allowed_values[key]}"
                )


# Default schema for governance contexts (security‑relevant fields)
DEFAULT_METADATA_SCHEMA = MetadataSchema(
    allowed_keys={
        "source": str,
        "version": int,
        "department": str,
        "request_id": str,
        # "sensitivity" is now a first‑class field on OperationalContext,
        # so we disallow it in metadata.
    },
    allowed_values={
        "source": {"yaml", "api", "manual", "cli"},
    },
    required_keys={"source"},
)
