import pytest
from unittest.mock import Mock

from query.execution import StageValidator
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


def test_valid_stage():
    validator = StageValidator()
    stage = DummyStage("test")
    validator.validate(stage)  # should not raise


def test_invalid_type():
    validator = StageValidator()
    with pytest.raises(TypeError):
        validator.validate(object())


def test_empty_name():
    validator = StageValidator()
    stage = DummyStage("")
    with pytest.raises(ValueError, match="cannot be empty"):
        validator.validate(stage)


def test_missing_execute():
    validator = StageValidator()
    stage = Mock(spec=Stage)
    stage.name = "test"
    # remove execute method
    del stage.execute
    with pytest.raises(ValueError, match="must define execute"):
        validator.validate(stage)


def test_is_valid():
    validator = StageValidator()
    stage = DummyStage("test")
    assert validator.is_valid(stage) is True
    assert validator.is_valid(object()) is False
