# kernel/bootstrap/tests/test_registrar.py
import pytest
from unittest.mock import Mock

from kernel.bootstrap.registrar import Registrar
from kernel.bootstrap.exceptions import RegistrationError
from kernel.managers import EngineManager, RepositoryManager, WorkflowManager


class TestRegistrar:
    def test_register_engines(self):
        container = Mock()
        registrar = Registrar(container)
        engine_manager = EngineManager()

        registrations = [
            {"name": "test_engine", "class": "kernel.bootstrap.tests.test_loader.DummyClass", "capabilities": ["test"]}
        ]
        registrar.register_engines(engine_manager, registrations)
        assert engine_manager.has("test_engine") is True

    def test_register_engines_missing_class(self):
        container = Mock()
        registrar = Registrar(container)
        engine_manager = EngineManager()

        registrations = [{"name": "test_engine"}]
        with pytest.raises(RegistrationError):
            registrar.register_engines(engine_manager, registrations)

    def test_register_repositories(self):
        container = Mock()
        registrar = Registrar(container)
        repo_manager = RepositoryManager()

        registrations = [
            {"name": "test_repo", "class": "kernel.bootstrap.tests.test_loader.DummyClass"}
        ]
        registrar.register_repositories(repo_manager, registrations)
        assert repo_manager.has("test_repo") is True

    def test_register_workflows(self):
        container = Mock()
        registrar = Registrar(container)
        workflow_manager = WorkflowManager()

        registrations = [
            {"name": "test_workflow", "steps": [], "default": True}
        ]
        registrar.register_workflows(workflow_manager, registrations)
        assert workflow_manager.has("test_workflow") is True
