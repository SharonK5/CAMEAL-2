# kernel/providers/llm/tests/test_llm_contract.py
"""
Contract tests for LLM providers.
"""

import pytest
from kernel.providers.llm.llm_provider import LLMProvider
from kernel.providers.llm.implementations import OllamaProvider


class TestLLMContract:
    def test_provider_interface(self):
        provider = OllamaProvider()
        assert isinstance(provider, LLMProvider)

    def test_required_methods(self):
        provider = OllamaProvider()
        assert hasattr(provider, "generate")
        assert callable(provider.generate)
        assert hasattr(provider, "stream")
        assert callable(provider.stream)
        assert hasattr(provider, "chat")
        assert callable(provider.chat)
        assert hasattr(provider, "chat_stream")
        assert callable(provider.chat_stream)
        assert hasattr(provider, "model_name")
        assert callable(provider.model_name)
        assert hasattr(provider, "supports_streaming")
        assert callable(provider.supports_streaming)
