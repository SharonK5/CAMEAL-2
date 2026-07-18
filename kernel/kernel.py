# kernel/kernel.py
"""
CAMEAL Kernel (stub).
"""

from .container import Container


class Kernel:
    """Stub kernel class."""

    def __init__(self, container: Container):
        self._container = container

    @property
    def container(self):
        return self._container
