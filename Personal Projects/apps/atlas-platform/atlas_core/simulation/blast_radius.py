from typing import List
from atlas_core.graph.graph_builder import AtlasGraphStore


def simulate_failure(graph_store: AtlasGraphStore, failed_service: str) -> tuple[List[str], List[str]]:
    """
    Returns:
    - direct dependents: immediate upstream services that rely on failed_service
    - impacted services: all recursive upstream services likely affected
    """
    if failed_service not in graph_store.graph:
        return [], []

    direct_dependents = sorted(list(graph_store.graph.predecessors(failed_service)))

    impacted = set()
    stack = list(direct_dependents)

    while stack:
        current = stack.pop()
        if current in impacted:
            continue
        impacted.add(current)

        for upstream in graph_store.graph.predecessors(current):
            if upstream not in impacted:
                stack.append(upstream)

    return direct_dependents, sorted(list(impacted))