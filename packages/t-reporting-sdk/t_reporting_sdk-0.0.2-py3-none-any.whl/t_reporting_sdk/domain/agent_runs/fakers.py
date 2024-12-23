from random import randint
from typing import Optional

from t_reporting_sdk.domain.agent_runs.models import AgentRun


class AgentRunFaker:
    @staticmethod
    def provide(
        run_id: Optional[int] = None,
    ) -> AgentRun:
        fake_run_id = randint(1, 100)
        return AgentRun(
            run_id=fake_run_id if run_id is None else run_id,
        )