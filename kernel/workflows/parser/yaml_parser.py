# kernel/workflows/parser/yaml_parser.py
"""
YAML parser for workflow definitions.
"""

import yaml
from typing import Dict, Any, List

from ..base.workflow import Workflow
from ..base.step import Step
from ..base.exceptions import WorkflowValidationError


class WorkflowYAMLParser:
    """
    Parses workflow definitions from YAML.
    """

    @classmethod
    def parse(cls, yaml_content: str) -> Workflow:
        """
        Parse a YAML string into a Workflow object.

        Args:
            yaml_content: YAML string.

        Returns:
            Workflow: The parsed workflow.

        Raises:
            WorkflowValidationError: If the YAML is invalid.
        """
        try:
            data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise WorkflowValidationError(f"Invalid YAML: {e}") from e

        return cls._parse_dict(data)

    @classmethod
    def parse_file(cls, filepath: str) -> Workflow:
        """
        Parse a YAML file into a Workflow object.

        Args:
            filepath: Path to the YAML file.

        Returns:
            Workflow: The parsed workflow.

        Raises:
            WorkflowValidationError: If the file cannot be read or parsed.
        """
        try:
            with open(filepath, "r") as f:
                content = f.read()
        except IOError as e:
            raise WorkflowValidationError(f"Failed to read file: {e}") from e

        return cls.parse(content)

    @classmethod
    def _parse_dict(cls, data: Dict[str, Any]) -> Workflow:
        """Parse a dictionary into a Workflow object."""
        if "name" not in data:
            raise WorkflowValidationError("Workflow missing 'name' field")
        if "steps" not in data:
            raise WorkflowValidationError("Workflow missing 'steps' field")

        steps = []
        for idx, step_data in enumerate(data.get("steps", [])):
            if isinstance(step_data, str):
                steps.append(Step(name=step_data, plugin=step_data))
            elif isinstance(step_data, dict):
                name = step_data.get("name")
                plugin = step_data.get("plugin")
                if not name:
                    raise WorkflowValidationError(f"Step at index {idx} missing 'name'")
                if not plugin:
                    raise WorkflowValidationError(
                        f"Step '{name}' missing 'plugin' field"
                    )
                steps.append(
                    Step(
                        name=name,
                        plugin=plugin,
                        config=step_data.get("config", {}),
                        depends_on=step_data.get("depends_on"),
                        condition=step_data.get("condition"),
                        on_failure=step_data.get("on_failure", "fail"),
                        timeout=step_data.get("timeout"),
                    )
                )
            else:
                raise WorkflowValidationError(
                    f"Invalid step format at index {idx}: {step_data}"
                )

        return Workflow(
            name=data["name"],
            steps=steps,
            description=data.get("description"),
            version=str(data.get("version", "1.0.0")),  # ✅ Convert to string
            metadata=data.get("metadata", {}),
            default=data.get("default", False),
        )
