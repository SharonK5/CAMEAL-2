# kernel/providers/model/tests/test_mock_model_provider.py
import pytest

from kernel.providers.model.implementations.mock_model_provider import MockModelProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderError


class TestMockModelProvider:
    @pytest.fixture
    def provider(self):
        return MockModelProvider()

    def test_initial_state(self, provider):
        assert provider.is_loaded() is False

    def test_load(self, provider):
        provider.load("dummy_path")
        assert provider.is_loaded() is True
        assert provider.get() is not None

    def test_predict(self, provider):
        provider.load("dummy_path")
        result = provider.predict({"input": "test"})
        assert result == "mock prediction"

    def test_predict_with_custom_output(self, provider):
        provider.load("dummy_path")
        result = provider.predict({"input": "test"}, output="custom")
        assert result == "custom"

    def test_predict_not_loaded(self, provider):
        with pytest.raises(ProviderError):
            provider.predict({})

    def test_metadata(self, provider):
        provider.load("dummy_path")
        meta = provider.metadata()
        assert meta["name"] == "mock_model"
        assert meta["model_type"] == "mock"
