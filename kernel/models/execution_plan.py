# kernel/models/execution_plan.py
from dataclasses import dataclass, field
from typing import Tuple

@dataclass(frozen=True)
class ExecutionPlan:
    workflow_name: str
    engine_names: Tuple[str, ...] = field(default_factory=tuple)
    metadata: dict = field(default_factory=dict)

    @property
    def stages(self) -> Tuple[str, ...]:
        return self.engine_names

    def __len__(self) -> int:
        return len(self.engine_names)

    def __iter__(self):
        return iter(self.engine_names)
