import pytest
from pathlib import Path

from kernel.router import Router


@pytest.fixture
def route_file(tmp_path: Path) -> Path:
    """Create a minimal valid routes YAML file."""
    yaml_content = """
routes:
  test_action:
    component: test_component
    workflow: test_workflow
default:
  component: default_component
  workflow: default_workflow
"""
    file_path = tmp_path / "routes.yaml"
    file_path.write_text(yaml_content, encoding="utf-8")
    return file_path


def test_router_initialization(route_file: Path) -> None:
    router = Router(route_file)
    assert router is not None
    assert router.health()["routes_loaded"] == 1
    assert router.health()["default_route"] == "default_component"
