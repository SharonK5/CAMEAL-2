"""
kernel.registry
===============

Central service registry for the CAMEAL Kernel.

The registry is responsible for:

- Registering system modules
- Discovering services via `resolve()`
- Preventing duplicate registrations (raises on duplicate)
- Listing active modules
- Unregistering services (silently ignores missing keys)

The registry deliberately contains no business logic.
It only manages service references.
"""


class ServiceRegistry:
    """
    Kernel service registry.
    """

    def __init__(self):
        self._services = {}

    def register(self, name, component):
        if name in self._services:
            raise KeyError(f"Component '{name}' is already registered.")
        self._services[name] = component

    def resolve(self, name):
        if name not in self._services:
            raise KeyError(f"Component '{name}' is not registered.")
        return self._services[name]

    def unregister(self, name):
        self._services.pop(name, None)

    def list_services(self):
        return sorted(self._services.keys())


# Singleton instance used by the kernel
registry = ServiceRegistry()
