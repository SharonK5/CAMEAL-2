# kernel/orchestrator/orchestrator.py
"""
Public orchestrator API.

The orchestrator coordinates execution by selecting workflows,
building execution plans, dispatching engines, and propagating context.
"""

import logging
from typing import Optional, TYPE_CHECKING

from ..models import Request, Response, ExecutionPlan
from ..context import ExecutionContext
from ..events import EventBus
from ..lifecycle import Lifecycle, HealthStatus

from .router import Router
from .planner import Planner
from .validator import Validator
from .executor import Executor
from .dispatcher import Dispatcher
from .pipeline import Pipeline
from .exceptions import OrchestratorError, PlanValidationError, WorkflowNotFoundError

if TYPE_CHECKING:
    from ..managers import WorkflowManager, EngineManager, ContextManager

logger = logging.getLogger(__name__)


class Orchestrator(Lifecycle):
    """
    Main execution coordinator for the CAMEAL Kernel.

    The orchestrator is stateless and thread-safe. Each request
    is processed independently with its own execution context.

    The orchestrator delegates all computational work to registered engines.
    It does not perform retrieval, reasoning, monitoring, evaluation,
    learning, or adaptation.
    """

    def __init__(
        self,
        workflow_manager: "WorkflowManager",
        engine_manager: "EngineManager",
        context_manager: "ContextManager",
        event_bus: Optional[EventBus] = None,
        allow_duplicate_stages: bool = False,
    ) -> None:
        super().__init__()
        self._workflow_manager = workflow_manager
        self._engine_manager = engine_manager
        self._context_manager = context_manager
        self._event_bus = event_bus

        self._router = Router(workflow_manager)
        self._planner = Planner(workflow_manager)
        self._dispatcher = Dispatcher(engine_manager)
        self._executor = Executor(dispatcher=self._dispatcher, event_bus=event_bus)
        self._validator = Validator(
            engine_manager=engine_manager,
            allow_duplicates=allow_duplicate_stages,
        )
        self._running = False

    # ---------- Implementation of abstract Lifecycle method ----------
    def _on_health(self) -> bool:
        """Return True if orchestrator and all dependencies are healthy."""
        return self.health() == HealthStatus.HEALTHY

    # ---------- Public API ----------

    def execute(self, request: Request) -> Response:
        try:
            context = self._build_context(request)
            workflow_name = self._router.select_workflow(request, context)
            plan = self._planner.create_plan(workflow_name, str(request.request_id))
            pipeline = self._plan_to_pipeline(plan)
            self._validator.validate(pipeline)
            final_context = self._executor.execute(pipeline, context)
            return self._build_response(request, final_context)
        except (PlanValidationError, WorkflowNotFoundError) as e:
            logger.error(f"Validation error: {e}")
            self._publish_failure_event(request, e)
            raise OrchestratorError(f"Request validation failed: {e}") from e
        except Exception as e:
            logger.error(f"Execution error: {e}")
            self._publish_failure_event(request, e)
            raise OrchestratorError(f"Execution failed: {e}") from e

    def validate(self, request: Request) -> bool:
        try:
            context = self._build_context(request)
            workflow_name = self._router.select_workflow(request, context)
            plan = self._planner.create_plan(workflow_name, str(request.request_id))
            pipeline = self._plan_to_pipeline(plan)
            self._validator.validate(pipeline)
            return True
        except (PlanValidationError, WorkflowNotFoundError) as e:
            logger.warning(f"Validation failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise OrchestratorError(f"Validation failed: {e}") from e

    def health(self) -> HealthStatus:
        try:
            engine_health = self._engine_manager.health_all()
            if any(h == HealthStatus.UNHEALTHY for h in engine_health.values()):
                return HealthStatus.UNHEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

        try:
            if hasattr(self._workflow_manager, 'health'):
                wf_health = self._workflow_manager.health()
                if wf_health == HealthStatus.UNHEALTHY:
                    return HealthStatus.UNHEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

        try:
            if hasattr(self._context_manager, 'health'):
                ctx_health = self._context_manager.health()
                if ctx_health == HealthStatus.UNHEALTHY:
                    return HealthStatus.UNHEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

        return HealthStatus.HEALTHY

    # ---------- Lifecycle methods ----------
    def start(self) -> None:
        self._running = True
        logger.info("Orchestrator started")

    def stop(self) -> None:
        self._running = False
        logger.info("Orchestrator stopped")

    # ---------- Internal helpers ----------
    def _build_context(self, request: Request) -> ExecutionContext:
        return self._context_manager.build_from_request(request)

    def _plan_to_pipeline(self, plan: ExecutionPlan) -> Pipeline:
        if hasattr(plan, 'to_pipeline'):
            return plan.to_pipeline()
        stages = getattr(plan, 'engine_names', None)
        if stages is None:
            stages = getattr(plan, 'stages', [])
        return Pipeline(
            workflow_name=plan.workflow_name,
            stages=tuple(stages),
            metadata=getattr(plan, 'metadata', {}),
        )

    def _build_response(self, request: Request, final_context: ExecutionContext) -> Response:
        result = final_context.get('result', None)
        metadata = {
            'request_id': str(request.request_id),
            'status': 'success',
            'execution_time': final_context.get('elapsed_time', 0),
        }
        return Response(
            request_id=str(request.request_id),
            result=result,
            metadata=metadata,
            status=200,
        )

    def _publish_failure_event(self, request: Request, error: Exception) -> None:
        if self._event_bus:
            event = {
                'type': 'orchestrator.execution.failed',
                'request_id': str(request.request_id),
                'error': str(error),
                'workflow_name': getattr(request, 'workflow_name', None),
            }
            self._event_bus.publish(event)
