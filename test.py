from kernel.base import KernelComponent
from kernel.lifecycle import lifecycle
from kernel.registry import registry


class Dummy(KernelComponent):

    def __init__(self):
        super().__init__("dummy")

    def initialize(self):
        self._initialized = True

    def shutdown(self):
        self._initialized = False

    def reset(self):
        pass

    def health(self):
        return {
            "status": "healthy",
            "initialized": self.initialized
        }


registry.register("dummy", Dummy())

lifecycle.initialize()

print(lifecycle.health())

lifecycle.shutdown()
