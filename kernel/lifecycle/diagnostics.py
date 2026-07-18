# kernel/lifecycle/diagnostics.py
from typing import Dict, Any, List
from .health import HealthReport


class Diagnostics:
    """
    Aggregates diagnostics information from multiple components.
    """

    @staticmethod
    def aggregate(reports: Dict[str, HealthReport]) -> Dict[str, Any]:
        """
        Aggregate health reports into a single diagnostics object.
        """
        healthy = 0
        degraded = 0
        unhealthy = 0
        unknown = 0
        components = []

        for name, report in reports.items():
            components.append(report.to_dict())
            if report.healthy:
                healthy += 1
            elif report.status.value == "degraded":
                degraded += 1
            elif report.status.value == "unhealthy":
                unhealthy += 1
            else:
                unknown += 1

        total = len(reports)
        overall = "healthy" if healthy == total else "degraded" if unhealthy == 0 else "unhealthy"

        return {
            "overall": overall,
            "healthy": healthy,
            "degraded": degraded,
            "unhealthy": unhealthy,
            "unknown": unknown,
            "total": total,
            "components": components,
        }
