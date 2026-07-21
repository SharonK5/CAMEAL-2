# kernel/providers/embedding/implementations/__init__.py
"""
Concrete embedding provider implementations.
"""

from .sentence_transformer import SentenceTransformerProvider

__all__ = ["SentenceTransformerProvider"]
