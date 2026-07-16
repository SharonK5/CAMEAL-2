import pytest

from query.execution import StageRegistry, StageResolver, StageBuilder, Pipeline
from query.execution.stage import Stage
from query.execution.contracts import StageResult


class DummyStage(Stage):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def execute(self, request, context) -> StageResult:
        return StageResult(success=True, stage=self.name)


def test_build():
    registry = StageRegistry()
    registry.register(DummyStage("validation"))
    registry.register(DummyStage("security"))

    resolver = StageResolver(registry)
    builder = StageBuilder(resolver)

    pipeline = builder.build(("validation", "security"))
    assert isinstance(pipeline, Pipeline)
    assert len(pipeline.stages) == 2


def test_build_all():
    registry = StageRegistry()
    registry.register(DummyStage("a"))
    registry.register(DummyStage("b"))

    resolver = StageResolver(registry)
    builder = StageBuilder(resolver)

    pipeline = builder.build_all()
    assert len(pipeline.stages) == 2


def test_unknown_stage():
    registry = StageRegistry()
    resolver = StageResolver(registry)
    builder = StageBuilder(resolver)

    with pytest.raises(KeyError):
        builder.build(("missing",))
