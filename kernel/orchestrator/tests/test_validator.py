# kernel/orchestrator/tests/test_validator.py
"""Tests for the Validator component."""

import pytest
from unittest.mock import Mock

from kernel.orchestrator.validator import Validator
from kernel.orchestrator.pipeline import Pipeline
from kernel.orchestrator.exceptions import PlanValidationError


class TestValidator:
    def test_validate_valid_pipeline(self):
        """Should not raise for a valid pipeline."""
        engine_manager = Mock()
        engine_manager.has.return_value = True

        validator = Validator(engine_manager)
        pipeline = Pipeline(
            workflow_name="test",
            stages=("security", "retrieval"),
        )
        validator.validate(pipeline)

    def test_validate_empty_pipeline(self):
        """Should raise if pipeline is empty."""
        engine_manager = Mock()
        validator = Validator(engine_manager)
        pipeline = Pipeline(workflow_name="test", stages=())

        with pytest.raises(PlanValidationError):
            validator.validate(pipeline)

    def test_validate_missing_engine(self):
        """Should raise if an engine is not registered."""
        engine_manager = Mock()
        engine_manager.has.side_effect = lambda name: name != "missing"

        validator = Validator(engine_manager)
        pipeline = Pipeline(workflow_name="test", stages=("security", "missing"))

        with pytest.raises(PlanValidationError):
            validator.validate(pipeline)

    def test_validate_duplicate_stages_not_allowed(self):
        """Should raise on duplicate stages by default."""
        engine_manager = Mock()
        engine_manager.has.return_value = True

        validator = Validator(engine_manager, allow_duplicates=False)
        pipeline = Pipeline(
            workflow_name="test",
            stages=("security", "retrieval", "security"),
        )

        with pytest.raises(PlanValidationError):
            validator.validate(pipeline)

    def test_validate_duplicate_stages_allowed(self):
        """Should allow duplicates when configured."""
        engine_manager = Mock()
        engine_manager.has.return_value = True

        validator = Validator(engine_manager, allow_duplicates=True)
        pipeline = Pipeline(
            workflow_name="test",
            stages=("security", "retrieval", "security"),
        )
        validator.validate(pipeline)  # No exception
