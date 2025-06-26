from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from lilac.domain.models import Resource


@dataclass(slots=True)
class PlanAction:
    """A single create/update/delete action."""

    action: str
    resource: Resource


def diff_resources(
    desired: Sequence[Resource], actual: Sequence[Resource]
) -> list[PlanAction]:
    """Return a list of actions to reconcile ``actual`` with ``desired``."""
    actions: list[PlanAction] = []
    actual_map: dict[tuple[str, str], Resource] = {
        (r.resource_type, r.namespace): r for r in actual if not r.ignore
    }

    for res in desired:
        if res.ignore:
            continue
        key = (res.resource_type, res.namespace)
        live = actual_map.pop(key, None)
        if live is None:
            actions.append(PlanAction("create", res))
        elif live.properties != res.properties:
            actions.append(PlanAction("update", res))

    for remaining in actual_map.values():
        actions.append(PlanAction("delete", remaining))

    return actions
