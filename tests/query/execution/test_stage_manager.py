import pytest
from unittest.mock import Mock

from query.execution import StageManager, ExecutionStage
from query.execution.contracts import StageResult


class DummyStage(ExecutionStage):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def execute(self, request, context) -> StageResult:
        return StageResult(success=True, stage=self.name)


def test_register_and_get():
    manager = StageManager()
    stage = DummyStage("test")
    manager.register(stage)
    assert manager.get("test") is stage


def test_contains():
    manager = StageManager()
    stage = DummyStage("test")
    manager.register(stage)
    assert manager.contains("test") is True
    assert manager.contains("missing") is False


def test_build_pipeline():
    manager = StageManager()
    s1 = DummyStage("a")
    s2 = DummyStage("b")
    manager.register(s1)
    manager.register(s2)
    pipeline = manager.build(("a", "b"))
    assert len(pipeline.stages) == 2
    assert pipeline.stages[0] is s1
    assert pipeline.stages[1] is s2


def test_build_all():
    manager = StageManager()
    s1 = DummyStage("a")
    s2 = DummyStage("b")
    manager.register(s1)
    manager.register(s2)
    pipeline = manager.build_all()
    assert len(pipeline.stages) == 2


def test_list_stages():
    manager = StageManager()
    s1 = DummyStage("a")
    s2 = DummyStage("b")
    manager.register(s1)
    manager.register(s2)
    assert set(manager.identifiers()) == {"a", "b"}
    assert set(manager.stages()) == {s1, s2}


def test_clear():
    manager = StageManager()
    manager.register(DummyStage("a"))
    assert manager.size() == 1
    manager.clear()
    assert manager.size() == 0


def test_duplicate_raises():
    manager = StageManager()
    stage = DummyStage("test")
    manager.register(stage)
    with pytest.raises(ValueError, match="already registered"):
        manager.register(DummyStage("test"))
