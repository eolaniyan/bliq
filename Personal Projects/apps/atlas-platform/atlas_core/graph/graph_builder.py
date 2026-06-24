import networkx as nx
from typing import List, Dict, Any
from atlas_core.models import ServiceDependency, ServiceNode


class AtlasGraphStore:
    """
    In-memory graph store for MVP.
    Later this can be replaced with Neo4j.
    """

    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        self.company_name: str | None = None

    def clear(self) -> None:
        self.graph.clear()
        self.company_name = None

    def add_service(self, node: ServiceNode) -> None:
        self.graph.add_node(
            node.name,
            node_type=node.service_type,
            metadata=node.metadata,
        )

    def add_dependency(self, dep: ServiceDependency) -> None:
        self.graph.add_edge(
            dep.source,
            dep.target,
            relationship=dep.relationship,
            confidence=dep.confidence,
            evidence_sources=dep.evidence_sources,
        )

    def get_services(self) -> List[str]:
        return sorted(list(self.graph.nodes))

    def get_dependencies(self, service_name: str) -> List[str]:
        if service_name not in self.graph:
            return []
        return sorted(list(self.graph.successors(service_name)))

    def get_dependents(self, service_name: str) -> List[str]:
        if service_name not in self.graph:
            return []
        return sorted(list(self.graph.predecessors(service_name)))

    def get_dependency_details(self, service_name: str) -> List[Dict[str, Any]]:
        if service_name not in self.graph:
            return []

        results: List[Dict[str, Any]] = []
        for target in sorted(self.graph.successors(service_name)):
            edge_data = self.graph.get_edge_data(service_name, target) or {}
            results.append(
                {
                    "source": service_name,
                    "target": target,
                    "relationship": edge_data.get("relationship", "CALLS"),
                    "confidence": edge_data.get("confidence", 0.0),
                    "evidence_sources": edge_data.get("evidence_sources", []),
                }
            )
        return results

    def get_dependent_details(self, service_name: str) -> List[Dict[str, Any]]:
        if service_name not in self.graph:
            return []

        results: List[Dict[str, Any]] = []
        for source in sorted(self.graph.predecessors(service_name)):
            edge_data = self.graph.get_edge_data(source, service_name) or {}
            results.append(
                {
                    "source": source,
                    "target": service_name,
                    "relationship": edge_data.get("relationship", "CALLS"),
                    "confidence": edge_data.get("confidence", 0.0),
                    "evidence_sources": edge_data.get("evidence_sources", []),
                }
            )
        return results

    def edge_count(self) -> int:
        return self.graph.number_of_edges()

    def node_count(self) -> int:
        return self.graph.number_of_nodes()