# kernel/workflows/tests/test_registry.py
import pytest

from kernel.workflows.registry.workflow_registry import WorkflowRegistry
from kernel.workflows.base.workflow import Workflow
from kernel.workflows.base.exceptions import WorkflowNotFoundError, WorkflowValidationError


class TestWorkflowRegistry:
    @pytest.fixture
    def registry(self):
        return WorkflowRegistry()

    @pytest.fixture
    def workflow(self):
        return Workflow(name="test", steps=[])

    def test_register_get(self, registry, workflow):
        registry.register(workflow)
        retrieved = registry.get("test")
        assert retrieved is workflow

    def test_register_duplicate(self, registry, workflow):
        registry.register(workflow)
        with pytest.raises(WorkflowValidationError):
            registry.register(workflow)

    def test_get_not_found(self, registry):
        with pytest.raises(WorkflowNotFoundError):
            registry.get("unknown")

    def test_has(self, registry, workflow):
        assert registry.has("test") is False
        registry.register(workflow)
        assert registry.has("test") is True

    def test_list(self, registry, workflow):
        assert registry.list() == []
        registry.register(workflow)
        assert registry.list() == ["test"]

    def test_len(self, registry, workflow):
        assert len(registry) == 0
        registry.register(workflow)
        assert len(registry) == 1

    def test_default(self, registry):
        w1 = Workflow(name="w1", steps=[])
        w2 = Workflow(name="w2", steps=[])
        registry.register(w1)
        registry.register(w2, default=True)
        assert registry.get_default().name == "w2"

    def test_default_single(self, registry):
        w1 = Workflow(name="w1", steps=[])
        registry.register(w1)
        assert registry.get_default().name == "w1"
