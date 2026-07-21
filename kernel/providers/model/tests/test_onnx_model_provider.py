# kernel/providers/model/tests/test_onnx_model_provider.py
import pytest
import tempfile
import os
import numpy as np

from kernel.providers.model.implementations.onnx_model_provider import ONNXModelProvider
from kernel.lifecycle import HealthStatus


class TestONNXModelProvider:
    @pytest.fixture
    def provider(self):
        return ONNXModelProvider()

    def test_initial_state(self, provider):
        assert provider.is_loaded() is False
        assert provider.health() == HealthStatus.UNHEALTHY

    def test_load_nonexistent(self, provider):
        with pytest.raises(Exception):  # Should raise ProviderInitializationError
            provider.load("/nonexistent/model.onnx")

    # Skipping actual ONNX test because it requires a real model file.
    # This test is just to show the pattern.
    @pytest.mark.skip("Requires ONNX model file")
    def test_load_and_predict(self, provider):
        # Create a simple ONNX model for testing
        # For demonstration, we assume we have a test model
        with tempfile.NamedTemporaryFile(suffix=".onnx", delete=False) as f:
            # Placeholder - in real test you'd generate a simple ONNX model
            pass

        # Not actually implemented for CI; we just show the pattern
        provider.load(f.name)
        assert provider.is_loaded() is True
        result = provider.predict(np.array([[1.0, 2.0]]))
        assert result is not None
        os.unlink(f.name)
