# kernel/providers/embedding/tests/test_sentence_transformer.py
import pytest

from kernel.providers.embedding.implementations.sentence_transformer import SentenceTransformerProvider
from kernel.lifecycle import HealthStatus


class TestSentenceTransformerProvider:
    @pytest.fixture
    def provider(self):
        """Create a provider instance for testing."""
        provider = SentenceTransformerProvider(
            model_name="all-MiniLM-L6-v2",
            device="cpu",
        )
        return provider

    def test_initial_state(self):
        """Provider should be unhealthy before initialization."""
        provider = SentenceTransformerProvider()
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_start_and_stop(self, provider):
        """Provider should become healthy after start and unhealthy after stop."""
        provider.start()
        assert provider.health() == HealthStatus.HEALTHY
        assert provider.dimension == 384

        provider.stop()
        assert provider.health() == HealthStatus.UNHEALTHY
        with pytest.raises(Exception):
            _ = provider.dimension

    def test_embed_single_text(self, provider):
        """Should embed a single text."""
        provider.start()
        embedding = provider.embed("Hello world")
        assert len(embedding) == 1
        assert len(embedding[0]) == provider.dimension
        provider.stop()

    def test_embed_multiple_texts(self, provider):
        """Should embed multiple texts."""
        provider.start()
        texts = ["Hello world", "Goodbye world", "Test sentence"]
        embeddings = provider.embed(texts)
        assert len(embeddings) == 3
        assert all(len(e) == provider.dimension for e in embeddings)
        provider.stop()

    def test_embed_query(self, provider):
        """Should embed a query."""
        provider.start()
        embedding = provider.embed_query("Search query")
        assert len(embedding) == provider.dimension
        provider.stop()

    def test_batch_size(self, provider):
        """Should return and set batch size."""
        provider.start()
        assert provider.batch_size() == 32
        provider.set_batch_size(64)
        assert provider.batch_size() == 64
        with pytest.raises(ValueError):
            provider.set_batch_size(0)
        provider.stop()

    def test_get_client(self, provider):
        """Should return the underlying model."""
        provider.start()
        model = provider.get()
        assert model is not None
        assert hasattr(model, "encode")
        provider.stop()
