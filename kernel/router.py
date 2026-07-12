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

        with open(route_file, encoding="utf-8") as stream:

            config = yaml.safe_load(stream)

        self._routes = config["routes"]

        self._default = config["default"]

        logger.info("Loaded %d routes.", len(self._routes))

    def resolve(self, request: Request) -> Route:

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

        self.load(route_file)

    def health(self) -> dict:

        return {
            "status": "healthy",
            "routes": len(self._routes),
        }
