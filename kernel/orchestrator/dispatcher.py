# kernel/orchestrator/dispatcher.py
"""
Internal dispatcher component.

Resolves and invokes engines by name.
"""

from ..managers import EngineManager
from ..context import ExecutionContext
from .exceptions import EngineNotFoundError, DispatcherError


class Dispatcher:
    """
    Dispatches execution to registered engines.
    """

    def __init__(self, engine_manager: EngineManager) -> None:
        self._engine_manager = engine_manager

    def dispatch(self, engine_name: str, context: ExecutionContext) -> ExecutionContext:
        """
        Invoke the named engine with the given context.

        Args:
            engine_name: The name of the engine to invoke.
            context: The immutable execution context.

        Returns:
            ExecutionContext: The updated context returned by the engine.

        Raises:
            EngineNotFoundError: If the engine is not registered.
            DispatcherError: If the invocation fails.
        """
        engine = self._engine_manager.get(engine_name)
        if not engine:
            raise EngineNotFoundError(f"Engine '{engine_name}' not registered")

        try:
            # Assume engines have an execute() method that takes context and returns context
            updated_context = engine.execute(context)
            return updated_context
        except Exception as e:
            raise DispatcherError(f"Engine '{engine_name}' execution failed: {e}") from e
