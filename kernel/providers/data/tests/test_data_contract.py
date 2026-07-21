# kernel/providers/data/tests/test_data_contract.py
"""
Contract tests for data providers.
"""

import pytest
from kernel.providers.data.data_provider import DataProvider
from kernel.providers.data.implementations import MockDataProvider


class TestDataContract:
    def test_provider_interface(self):
        provider = MockDataProvider()
        assert isinstance(provider, DataProvider)

    def test_required_methods(self):
        provider = MockDataProvider()
        assert hasattr(provider, "fetch")
        assert callable(provider.fetch)
        assert hasattr(provider, "mutate")
        assert callable(provider.mutate)
        assert hasattr(provider, "query")
        assert callable(provider.query)
        assert hasattr(provider, "execute")
        assert callable(provider.execute)
