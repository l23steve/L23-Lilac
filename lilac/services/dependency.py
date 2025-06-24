from __future__ import annotations

from typing import Sequence

from lilac.domain.dependency import build_graph, order_resources
from lilac.domain.models import Resource


def plan_resources(resources: Sequence[Resource]) -> list[Resource]:
    """Order resources respecting their dependencies."""
    graph = build_graph(resources)
    return order_resources(graph)
