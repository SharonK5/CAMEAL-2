# kernel/bootstrap/tests/test_discovery.py
import pytest
import tempfile
import os

from kernel.bootstrap.discovery import Discovery
from kernel.bootstrap.exceptions import DiscoveryError


class TestDiscovery:
    def test_discover_plugins(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a manifest file
            manifest_path = os.path.join(tmpdir, "manifest.yaml")
            with open(manifest_path, 'w') as f:
                f.write("name: test")
            manifests = Discovery.discover_plugins(tmpdir)
            assert len(manifests) == 1
            assert manifests[0] == manifest_path

    def test_discover_packages(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a package with __init__.py
            pkg_path = os.path.join(tmpdir, "test_pkg")
            os.makedirs(pkg_path)
            with open(os.path.join(pkg_path, "__init__.py"), 'w') as f:
                f.write("")
            packages = Discovery.discover_packages(tmpdir)
            assert "test_pkg" in packages
