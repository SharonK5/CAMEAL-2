# kernel/providers/vector/implementations/__init__.py
"""
Concrete vector store implementations.
"""

from .faiss_vector_store import FAISSVectorStoreProvider

__all__ = ["FAISSVectorStoreProvider"]
