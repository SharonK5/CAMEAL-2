# kernel/providers/embedding/tests/test_embedding_contract.py
import pytest
from kernel.providers.embedding.embedding_provider import EmbeddingProvider
from kernel.providers.embedding.implementations.sentence_transformer import SentenceTransformerProvider
from kernel.lifecycle import HealthStatus


class TestEmbeddingContract:
    def test_provider_interface(self):
        provider = SentenceTransformerProvider()
        assert isinstance(provider, EmbeddingProvider)

    def test_required_methods(self):
        provider = SentenceTransformerProvider()
        # Check that the class defines the property 'dimension'
        assert hasattr(SentenceTransformerProvider, 'dimension')
        assert hasattr(provider, "embed")
        assert callable(provider.embed)
        assert hasattr(provider, "embed_query")
        assert callable(provider.embed_query)
        assert hasattr(provider, "batch_size")
        assert callable(provider.batch_size)

    @pytest.mark.skipif(
        not hasattr(SentenceTransformerProvider, "_model"),
        reason="SentenceTransformerProvider not available"
    )
    def test_concrete_provider(self):
        provider = SentenceTransformerProvider()
        provider.start()
        try:
            assert provider.health() == HealthStatus.HEALTHY
            embedding = provider.embed("test")
            assert len(embedding) == 1
            assert len(embedding[0]) == provider.dimension
        finally:
            provider.stop()
