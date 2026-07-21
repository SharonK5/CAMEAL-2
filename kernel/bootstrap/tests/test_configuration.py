# kernel/bootstrap/tests/test_configuration.py
import pytest
import tempfile
import os
import json
import yaml

from kernel.bootstrap import Configuration
from kernel.bootstrap.exceptions import ConfigurationError


class TestConfiguration:
    def test_load_dict(self):
        config = Configuration()
        data = {"test": "value"}
        config.load(data)
        assert config.get("test") == "value"

    def test_load_json_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"test": "value"}, f)
            f.close()
            config = Configuration()
            config.load(f.name)
            assert config.get("test") == "value"
            os.unlink(f.name)

    def test_load_yaml_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump({"test": "value"}, f)
            f.close()
            config = Configuration()
            config.load(f.name)
            assert config.get("test") == "value"
            os.unlink(f.name)

    def test_load_invalid_file(self):
        config = Configuration()
        with pytest.raises(ConfigurationError):
            config.load("/nonexistent/file.yaml")

    def test_get_nested(self):
        config = Configuration()
        config.load({"a": {"b": {"c": "value"}}})
        assert config.get("a.b.c") == "value"
        assert config.get("a.b.d", "default") == "default"
