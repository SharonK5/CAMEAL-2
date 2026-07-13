from pathlib import Path

import yaml

from kernel.request import Request
from kernel.router import Router


def test_router_initialization(tmp_path: Path):
    """Test Router initialization."""

    routes = {
        "routes": {
            "query": {
                "component": "repository",
                "workflow": "authoritative",
                "priority": 10,
                "authentication": True,
                "governance": False,
            }
        },
        "default": {
            "component": "repository"
        },
    }

    route_file = tmp_path / "routes.yaml"

    route_file.write_text(
        yaml.safe_dump(routes),
        encoding="utf-8",
    )

    router = Router(route_file)

    request = Request(action="query")

    route = router.resolve(request)

    assert route.component == "repository"
    assert route.workflow == "authoritative"
    assert route.priority == 10
    assert route.authentication is True
