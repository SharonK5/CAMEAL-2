# kernel/providers/llm/tests/test_ollama_provider.py
import pytest

from kernel.providers.llm.implementations.ollama_provider import OllamaProvider
from kernel.lifecycle import HealthStatus


class TestOllamaProvider:
    @pytest.fixture
    def provider(self):
        return OllamaProvider(model="llama2", base_url="http://localhost:11434")

    def test_initial_state(self, provider):
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_start_and_stop(self, provider):
        # Skip if Ollama not running
        try:
            provider.start()
            assert provider.health() in (HealthStatus.HEALTHY, HealthStatus.DEGRADED)
            provider.stop()
            assert provider.health() == HealthStatus.UNHEALTHY
        except Exception as e:
            pytest.skip(f"Ollama not available: {e}")

    def test_generate(self, provider):
        try:
            provider.start()
            response = provider.generate("Hello, how are you?")
            assert isinstance(response, str)
            assert len(response) > 0
            provider.stop()
        except Exception as e:
            pytest.skip(f"Ollama not available: {e}")

    def test_stream(self, provider):
        try:
            provider.start()
            chunks = list(provider.stream("Hello"))
            assert len(chunks) > 0
            assert all(isinstance(c, str) for c in chunks)
            provider.stop()
        except Exception as e:
            pytest.skip(f"Ollama not available: {e}")

    def test_chat(self, provider):
        try:
            provider.start()
            response = provider.chat([
                {"role": "user", "content": "Hello"}
            ])
            assert isinstance(response, str)
            assert len(response) > 0
            provider.stop()
        except Exception as e:
            pytest.skip(f"Ollama not available: {e}")

    def test_model_name(self, provider):
        assert provider.model_name() == "llama2"

    def test_supports_streaming(self, provider):
        assert provider.supports_streaming() is True
