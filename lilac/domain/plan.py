from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

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


def _resource_key(res: Resource) -> tuple[str, str, Any]:
    """Return a unique key for ``res`` used for diffing."""
    props = _strip_details(res.properties)
    ident = props.get("id") or props.get("arn") or props.get("name")
    return (res.resource_type, res.namespace, ident)


def diff_resources(
    desired: Sequence[Resource], actual: Sequence[Resource]
) -> list[PlanAction]:
    """Return a list of actions to reconcile ``actual`` with ``desired``."""
    actions: list[PlanAction] = []
    actual_map: dict[tuple[str, str, Any], Resource] = {
        _resource_key(r): r for r in actual if not r.ignore
    }

    for res in desired:
        if res.ignore:
            continue
        key = _resource_key(res)
        live = actual_map.pop(key, None)
        if live is None:
            actions.append(PlanAction("create", res))
        elif _strip_details(live.properties) != _strip_details(res.properties):
            actions.append(PlanAction("update", res))

    for remaining in actual_map.values():
        actions.append(PlanAction("delete", remaining))

    return actions
