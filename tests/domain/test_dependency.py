from __future__ import annotations

import networkx as nx
import pytest

from lilac.domain.dependency import (
    DependencyCycleError,
    build_graph,
    order_resources,
)
from lilac.domain.models import Resource


def _res(name: str, deps: list[str] | None = None) -> Resource:
    return Resource(
        resource_type=name,
        namespace="default",
        depends_on=deps or [],
        properties={},
    )


def test_build_and_order_graph() -> None:
    r1 = _res("one")
    r2 = _res("two", ["one"])
    r3 = _res("three", ["two"])

    graph = build_graph([r1, r2, r3])

    assert isinstance(graph, nx.DiGraph)
    ordered = order_resources(graph)
    assert ordered == [r1, r2, r3]


def test_cycle_detection() -> None:
    r1 = _res("one", ["two"])
    r2 = _res("two", ["one"])

    graph = build_graph([r1, r2])

    with pytest.raises(DependencyCycleError):
        order_resources(graph)
