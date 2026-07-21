# kernel/plugins/tests/test_plugin.py
import pytest
from kernel.plugins.base.plugin import Plugin
from kernel.lifecycle import Lifecycle


class TestPluginInterface:
    def test_plugin_subclasses_lifecycle(self):
        assert issubclass(Plugin, Lifecycle)

    def test_plugin_abstract_methods(self):
        # Try to instantiate without implementing abstract methods
        with pytest.raises(TypeError):
            Plugin()
