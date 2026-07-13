"""
===============================================================================
Module: kernel.router

Configuration-driven router.

Author: Sharon Kaitano
Project: CAMEAL
License: MIT
===============================================================================
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from .request import Request
from .route import Route
from .validators import RequestValidator

logger = logging.getLogger(__name__)


class Router:
    """
    Configuration-driven request router.
    """

    def __init__(self, route_file: Path):

        self._validator = RequestValidator()

        self._routes: dict = {}

        self._default: dict = {}

        self.load(route_file)

    def load(self, route_file: Path) -> None:
        """
        Load route configuration from a YAML file.
        """
        config = yaml.safe_load(
            route_file.read_text(encoding="utf-8")
        )

        self._routes = config["routes"]
        self._default = config["default"]

        logger.info("Loaded %d routes.", len(self._routes))

    def resolve(self, request: Request) -> Route:
        """
        Resolve a Request to a Route based on its action.
        """
        self._validator.validate(request)

        config = self._routes.get(
            request.action,
            self._default,
        )

        return Route(
            action=request.action,
            component=config["component"],
            workflow=config.get("workflow"),
            priority=config.get("priority", 100),
            authentication=config.get(
                "authentication",
                False,
            ),
            governance=config.get(
                "governance",
                False,
            ),
        )

    def reload(self, route_file: Path) -> None:
        """
        Reload the route configuration from a file.
        """
        self.load(route_file)

    def health(self) -> dict:
        """
        Return health and status information about the router.
        """
        return {
            "status": "healthy",
            "routes_loaded": len(self._routes),
            "default_route": self._default.get("component"),
            "validator": self._validator.__class__.__name__,
        }
