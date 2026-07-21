# kernel/workflows/parser/json_parser.py
"""
JSON parser for workflow definitions.
"""

import json
from typing import Dict, Any

from ..base.workflow import Workflow
from ..base.exceptions import WorkflowValidationError


class WorkflowJSONParser:
    """
    Parses workflow definitions from JSON.
    """

    @classmethod
    def parse(cls, json_content: str) -> Workflow:
        """
        Parse a JSON string into a Workflow object.

        Args:
            json_content: JSON string.

        Returns:
            Workflow: The parsed workflow.

        Raises:
            WorkflowValidationError: If the JSON is invalid.
        """
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError as e:
            raise WorkflowValidationError(f"Invalid JSON: {e}") from e

        # Reuse the YAML parser's dict parsing logic
        from .yaml_parser import WorkflowYAMLParser
        return WorkflowYAMLParser._parse_dict(data)

    @classmethod
    def parse_file(cls, filepath: str) -> Workflow:
        """
        Parse a JSON file into a Workflow object.

        Args:
            filepath: Path to the JSON file.

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
