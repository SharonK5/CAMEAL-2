# kernel/bootstrap/tests/test_builder.py
import pytest
from unittest.mock import Mock, patch

from kernel.bootstrap.builder import Builder
from kernel.bootstrap.configuration import Configuration


class TestBuilder:
    def test_build_container(self):
        config = Configuration()
        builder = Builder(config)
        container = builder.build_container()
        assert container is not None

    def test_build_core_services(self):
        config = Configuration()
        builder = Builder(config)
        builder.build_container()
        builder.build_core_services()
        assert builder._event_bus is not None
        assert builder._context_builder is not None

    def test_build_managers(self):
        config = Configuration()
        builder = Builder(config)
        builder.build_container()
        builder.build_managers()
        assert builder._engine_manager is not None
        assert builder._repository_manager is not None
        assert builder._workflow_manager is not None

    def test_build_orchestrator(self):
        config = Configuration()
        builder = Builder(config)
        builder.build_container()
        builder.build_managers()
        orchestrator = builder.build_orchestrator()
        assert orchestrator is not None

    def test_validate_runtime(self):
        config = Configuration()
        # Register a minimal workflow so the validator passes
        config.load({
            "workflow_registrations": [
                {"name": "default", "steps": [], "default": True}
            ]
        })
        builder = Builder(config)
        builder.build_container()
        builder.build_managers()
        builder.register_components()  # This registers the workflow
        # Should not raise
        builder.validate_runtime()

    def test_build_kernel(self):
        config = Configuration()
        builder = Builder(config)
        kernel = builder.build_kernel()
        assert kernel is not None
