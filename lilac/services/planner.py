from __future__ import annotations

from pathlib import Path


from lilac.adapters import load_resources

from lilac.domain.plan import PlanAction, diff_resources
from lilac.services.scanner import scan_resources


def plan(directory: str | Path, namespace: str) -> list[PlanAction]:
    """Generate a plan for resources in ``directory`` within ``namespace``."""
    desired = load_resources(Path(directory))
    live = scan_resources(namespace)
    return diff_resources(desired, live)
