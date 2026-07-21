# kernel/workflows/tests/test_parser.py
import pytest

from kernel.workflows.parser.yaml_parser import WorkflowYAMLParser
from kernel.workflows.base.exceptions import WorkflowValidationError


class TestWorkflowYAMLParser:
    def test_parse_minimal(self):
        yaml = """
name: test
steps:
  - step1
  - step2
"""
        workflow = WorkflowYAMLParser.parse(yaml)
        assert workflow.name == "test"
        assert len(workflow) == 2
        assert workflow.steps[0].name == "step1"
        assert workflow.steps[0].plugin == "step1"

    def test_parse_full(self):
        yaml = """
name: full
description: Full workflow
version: 2.0
steps:
  - name: context
    plugin: context_plugin
    config:
      timeout: 30
  - name: process
    plugin: process_plugin
    depends_on: ["context"]
    on_failure: retry
    timeout: 60
"""
        workflow = WorkflowYAMLParser.parse(yaml)
        assert workflow.name == "full"
        assert workflow.description == "Full workflow"
        assert workflow.version == "2.0"
        assert len(workflow) == 2
        assert workflow.steps[0].config["timeout"] == 30
        assert workflow.steps[1].depends_on == ["context"]
        assert workflow.steps[1].on_failure == "retry"
        assert workflow.steps[1].timeout == 60

    def test_parse_missing_name(self):
        yaml = """
steps: []
"""
        with pytest.raises(WorkflowValidationError):
            WorkflowYAMLParser.parse(yaml)

    def test_parse_missing_steps(self):
        yaml = """
name: test
"""
        with pytest.raises(WorkflowValidationError):
            WorkflowYAMLParser.parse(yaml)

    def test_parse_invalid_yaml(self):
        with pytest.raises(WorkflowValidationError):
            WorkflowYAMLParser.parse("invalid: yaml: content: [bad")
