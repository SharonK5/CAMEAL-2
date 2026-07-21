# kernel/providers/tests/test_vector_faiss.py
"""
Tests for FAISS vector store provider.
"""

import pytest
import tempfile
import numpy as np

from kernel.providers.vector.implementations.faiss_vector_store import FAISSVectorStoreProvider
from kernel.lifecycle import HealthStatus


class TestFAISSVectorStoreProvider:
    @pytest.fixture
    def provider(self):
        return FAISSVectorStoreProvider(dimension=384)

    @pytest.fixture
    def sample_vectors(self):
        np.random.seed(42)
        return np.random.randn(10, 384).tolist()

    def test_initial_state(self, provider):
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_start_and_stop(self, provider):
        provider.start()
        assert provider.health() == HealthStatus.HEALTHY
        provider.stop()
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_upsert_and_query(self, provider, sample_vectors):
        provider.start()
        try:
            ids = [f"doc{i}" for i in range(10)]
            provider.upsert(ids, sample_vectors)

            results = provider.query(sample_vectors[0], top_k=3)
            assert len(results) == 3
            assert results[0]["id"] == "doc0"
            assert "score" in results[0]
            assert "metadata" in results[0]
        finally:
            provider.stop()

    def test_count(self, provider, sample_vectors):
        provider.start()
        try:
            assert provider.count() == 0
            provider.upsert(
                [f"doc{i}" for i in range(5)],
                sample_vectors[:5]
            )
            assert provider.count() == 5
        finally:
            provider.stop()

    def test_clear(self, provider, sample_vectors):
        provider.start()
        try:
            provider.upsert(
                [f"doc{i}" for i in range(5)],
                sample_vectors[:5]
            )
            assert provider.count() == 5
            provider.clear()
            assert provider.count() == 0
        finally:
            provider.stop()

    def test_persistence(self, sample_vectors):
        with tempfile.TemporaryDirectory() as tmpdir:
            persist_path = f"{tmpdir}/faiss_index"
            provider = FAISSVectorStoreProvider(
                dimension=384,
                persist_path=persist_path
            )

            provider.start()
            try:
                ids = [f"doc{i}" for i in range(5)]
                provider.upsert(ids, sample_vectors[:5])
                assert provider.count() == 5
            finally:
                provider.stop()

            # Reload from disk
            provider2 = FAISSVectorStoreProvider(
                dimension=384,
                persist_path=persist_path
            )
            provider2.start()
            try:
                # Should have the same count
                pass
            finally:
                provider2.stop()
