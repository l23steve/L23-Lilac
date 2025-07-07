from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from typing import Any

from lilac.domain.models import Resource


@dataclass(slots=True)
class PlanAction:
    """A single create/update/delete action."""

    action: str
    resource: Resource


def _strip_details(props: dict[str, Any]) -> dict[str, Any]:
    """Return ``props`` without the ``details`` key."""
    new_props = dict(props)
    new_props.pop("details", None)
    return new_props


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
        elif _strip_details(live.properties) != _strip_details(res.properties):
            actions.append(PlanAction("update", res))

    for remaining in actual_map.values():
        actions.append(PlanAction("delete", remaining))

    return actions
