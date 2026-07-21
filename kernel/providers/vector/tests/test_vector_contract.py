# kernel/providers/vector/tests/test_vector_contract.py
"""
Contract tests for vector providers.
"""

import pytest
import numpy as np

from kernel.providers.vector.vector_provider import VectorProvider
from kernel.providers.vector.implementations.faiss_vector_store import FAISSVectorStoreProvider


class TestVectorContract:
    def test_provider_interface(self):
        provider = FAISSVectorStoreProvider(dimension=384)
        assert isinstance(provider, VectorProvider)

    def test_required_methods(self):
        provider = FAISSVectorStoreProvider(dimension=384)
        assert hasattr(provider, "upsert")
        assert callable(provider.upsert)
        assert hasattr(provider, "query")
        assert callable(provider.query)
        assert hasattr(provider, "delete")
        assert callable(provider.delete)
        assert hasattr(provider, "get_by_id")
        assert callable(provider.get_by_id)
        assert hasattr(provider, "count")
        assert callable(provider.count)
        assert hasattr(provider, "dimension")
        assert callable(provider.dimension)
        assert hasattr(provider, "clear")
        assert callable(provider.clear)

    def test_dimension(self):
        provider = FAISSVectorStoreProvider(dimension=384)
        provider.start()
        try:
            assert provider.dimension() == 384
        finally:
            provider.stop()
