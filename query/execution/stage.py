"""
Compatibility layer.

Future imports should use BaseStage.
"""

from .base_stage import BaseStage

Stage = BaseStage
ExecutionStage = BaseStage   # preserve old name for compatibility

__all__ = [
    "BaseStage",
    "Stage",
    "ExecutionStage",
]
