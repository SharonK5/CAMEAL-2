# kernel/plugins/tests/test_discovery.py
import tempfile
import yaml
from pathlib import Path
from kernel.plugins.discovery import PluginDiscovery
from kernel.plugins.exceptions import PluginError


class TestPluginDiscovery:
    def test_discover(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.yaml"
            manifest_path.write_text("""
name: test
version: 1.0.0
""")
            manifests = PluginDiscovery.discover(tmpdir)
            assert len(manifests) == 1
            assert manifests[0].name == "test"
            assert manifests[0].version == "1.0.0"

    def test_discover_yml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.yml"
            manifest_path.write_text("""
name: test
version: 1.0.0
""")
            manifests = PluginDiscovery.discover(tmpdir)
            assert len(manifests) == 1

    def test_discover_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manifests = PluginDiscovery.discover(tmpdir)
            assert len(manifests) == 0

    def test_discover_invalid_yaml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.yaml"
            manifest_path.write_text("invalid yaml: [")
            try:
                PluginDiscovery.discover(tmpdir)
            except PluginError:
                pass
            else:
                assert False, "Expected PluginError"
