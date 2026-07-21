# kernel/managers/tests/test_plugin_manager.py
import pytest
from unittest.mock import Mock, patch

from kernel.managers import PluginManager
from kernel.container import Container


class TestPluginManager:
    def test_register(self):
        # Use a mock container instead of the abstract Container
        mock_container = Mock(spec=Container)
        mgr = PluginManager(mock_container)
        engine = Mock()
        mgr.register("test", engine)
        assert mgr.has("test") is True

    def test_list(self):
        mock_container = Mock(spec=Container)
        mgr = PluginManager(mock_container)
        engine1 = Mock()
        engine2 = Mock()
        mgr.register("plugin1", engine1)
        mgr.register("plugin2", engine2)
        assert sorted(mgr.list()) == ["plugin1", "plugin2"]
