from __future__ import annotations

from typing import Sequence

import networkx as nx

from lilac.domain.models import Resource


class DependencyCycleError(Exception):
    """Raised when a cyclic dependency is detected."""


def build_graph(resources: Sequence[Resource]) -> nx.DiGraph:
    """Create a dependency graph from a list of resources."""
    graph: nx.DiGraph = nx.DiGraph()

    # Map resource identifiers to Resource objects and create nodes
    resource_map: dict[str, Resource] = {}
    for res in resources:
        resource_map[res.resource_type] = res
        graph.add_node(res.resource_type, resource=res)

    for res in resources:
        for dep in res.depends_on:
            dep_key = dep
            dep_res = resource_map.get(dep_key)
            if dep_res is None:
                continue
            graph.add_edge(dep_res.resource_type, res.resource_type)
    return graph


def order_resources(graph: nx.DiGraph) -> list[Resource]:
    """Return resources ordered by dependencies."""
    if not nx.is_directed_acyclic_graph(graph):
        cycle = list(nx.simple_cycles(graph))
        raise DependencyCycleError(f"cyclic dependency detected: {cycle}")

    ordered: list[Resource] = []
    for node in nx.topological_sort(graph):
        ordered.append(graph.nodes[node]["resource"])
    return ordered
