from __future__ import annotations

from pathlib import Path
from typing import List

from lilac.domain.plan import PlanAction
from lilac.services.planner import plan as plan_changes


def deploy(
    directory: str | Path,
    namespace: str,
    dry_run: bool = False,
) -> List[PlanAction]:
    """Generate a plan and optionally apply it.

    In this reference implementation no real cloud operations are performed.
    When ``dry_run`` is ``True`` the function simply returns the planned
    actions without applying them. When ``False`` it would normally apply the
    changes but currently only returns the actions for integration purposes.
    """

    actions = plan_changes(directory, namespace)
    if dry_run:
        return actions

    # TODO: integrate with real deployment logic
    return actions
