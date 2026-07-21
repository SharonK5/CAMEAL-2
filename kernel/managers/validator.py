# kernel/managers/validator.py
"""
Generic validator for manager components.
"""

from typing import Any, Type
from .exceptions import ManagerValidationError


class Validator:
    """
    Generic validator for manager components.
    """

    @staticmethod
    def validate_name(name: str) -> None:
        if not name or not name.strip():
            raise ManagerValidationError("Name cannot be empty")

    @staticmethod
    def validate_type(instance: Any, expected_type: Type) -> None:
        if not isinstance(instance, expected_type):
            raise ManagerValidationError(
                f"Expected {expected_type.__name__}, got {type(instance).__name__}"
            )

    @staticmethod
    def validate_not_none(instance: Any, name: str = "instance") -> None:
        if instance is None:
            raise ManagerValidationError(f"{name} cannot be None")
