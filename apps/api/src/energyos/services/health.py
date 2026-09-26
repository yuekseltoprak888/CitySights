from typing import Literal

from energyos.domain.health import DatabaseStatus, HealthReport
from energyos.domain.ports import DatabaseProbe


class HealthService:
    def __init__(self, probe: DatabaseProbe, environment: str) -> None:
        self._probe = probe
        self._environment = environment

    def check(self) -> HealthReport:
        status = self._probe.check()
        overall = _overall_status(status)
        return HealthReport(
            status=overall,
            environment=self._environment,
            country="CH",
            database=status.database,
            postgis=status.postgis,
        )


def _overall_status(status: DatabaseStatus) -> Literal["ok", "degraded"]:
    if status.database == "ok" and status.postgis == "ok":
        return "ok"
    return "degraded"
