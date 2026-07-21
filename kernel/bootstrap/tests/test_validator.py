# kernel/bootstrap/tests/test_validator.py
import pytest
from unittest.mock import Mock

from kernel.bootstrap.validator import Validator
from kernel.bootstrap.exceptions import ValidationError


class TestValidator:
    def test_validate_container(self):
        container = Mock()
        Validator.validate_container(container)  # Should not raise

    def test_validate_container_none(self):
        with pytest.raises(ValidationError, match="Container is required"):
            Validator.validate_container(None)

    def test_validate_workflows_empty(self):
        workflow_manager = Mock()
        workflow_manager.__len__ = Mock(return_value=0)
        # The validator checks if workflow_manager is None first, then len
        with pytest.raises(ValidationError):
            Validator.validate_workflows(workflow_manager)

    def test_validate_workflows_with_workflow(self):
        workflow_manager = Mock()
        workflow_manager.__len__ = Mock(return_value=1)
        Validator.validate_workflows(workflow_manager)  # Should not raise
