# kernel/providers/model/tests/test_model_contract.py
"""
Contract tests for model providers.
"""

import pytest
from kernel.providers.model.model_provider import ModelProvider
from kernel.providers.model.implementations import MockModelProvider


class TestModelContract:
    def test_provider_interface(self):
        provider = MockModelProvider()
        assert isinstance(provider, ModelProvider)

    def test_required_methods(self):
        provider = MockModelProvider()
        assert hasattr(provider, "load")
        assert callable(provider.load)
        assert hasattr(provider, "predict")
        assert callable(provider.predict)
        assert hasattr(provider, "metadata")
        assert callable(provider.metadata)
        assert hasattr(provider, "is_loaded")
        assert callable(provider.is_loaded)
