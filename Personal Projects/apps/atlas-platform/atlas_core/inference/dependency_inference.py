from pathlib import Path
from typing import Dict, List, Set
import re

from atlas_core.ingestion.file_loader import load_json_files_in_dir, load_text_files_in_dir
from atlas_core.models import ServiceDependency, ServiceNode
from atlas_core.normalization.service_name_resolver import normalize_service_name


def _extract_services_from_repo_defs(repos_dir: Path) -> List[ServiceNode]:
    nodes: List[ServiceNode] = []
    repo_files = load_json_files_in_dir(repos_dir)

    for item in repo_files:
        service_name = normalize_service_name(item["service"])
        nodes.append(
            ServiceNode(
                name=service_name,
                metadata={
                    "repo": item.get("repo", f"{service_name}_repo"),
                    "domain": item.get("domain", "unknown"),
                },
            )
        )
    return nodes


def _extract_dependencies_from_repo_defs(repos_dir: Path) -> List[ServiceDependency]:
    dependencies: List[ServiceDependency] = []
    repo_files = load_json_files_in_dir(repos_dir)

    for item in repo_files:
        source = normalize_service_name(item["service"])
        for target in item.get("calls", []):
            dependencies.append(
                ServiceDependency(
                    source=source,
                    target=normalize_service_name(target),
                    relationship="CALLS",
                    confidence=0.75,
                    evidence_sources=["repo_config"],
                )
            )
    return dependencies


def _extract_dependencies_from_traces(traces_dir: Path) -> List[ServiceDependency]:
    dependencies: List[ServiceDependency] = []
    trace_files = load_json_files_in_dir(traces_dir)

    for trace in trace_files:
        services = [normalize_service_name(s) for s in trace.get("services", [])]
        for i in range(len(services) - 1):
            dependencies.append(
                ServiceDependency(
                    source=services[i],
                    target=services[i + 1],
                    relationship="CALLS",
                    confidence=0.9,
                    evidence_sources=["trace"],
                )
            )
    return dependencies


def _extract_dependencies_from_logs(logs_dir: Path, known_services: Set[str]) -> List[ServiceDependency]:
    dependencies: List[ServiceDependency] = []
    logs = load_text_files_in_dir(logs_dir)

    pattern = re.compile(r"calling\s+([a-zA-Z0-9_\-]+)", re.IGNORECASE)

    for filename, content in logs.items():
        source_name = normalize_service_name(filename.replace(".log", ""))
        for line in content.splitlines():
            match = pattern.search(line)
            if match:
                target = normalize_service_name(match.group(1))
                if target in known_services:
                    dependencies.append(
                        ServiceDependency(
                            source=source_name,
                            target=target,
                            relationship="CALLS",
                            confidence=0.85,
                            evidence_sources=["logs"],
                        )
                    )
    return dependencies


def merge_dependencies(deps: List[ServiceDependency]) -> List[ServiceDependency]:
    merged: Dict[tuple[str, str, str], ServiceDependency] = {}

    for dep in deps:
        key = (dep.source, dep.target, dep.relationship)
        if key not in merged:
            merged[key] = dep
        else:
            existing = merged[key]
            existing.confidence = min(0.99, max(existing.confidence, dep.confidence) + 0.05)
            existing.evidence_sources = sorted(list(set(existing.evidence_sources + dep.evidence_sources)))

    return list(merged.values())


def infer_company_graph(company_dir: Path) -> tuple[List[ServiceNode], List[ServiceDependency]]:
    repos_dir = company_dir / "repos"
    traces_dir = company_dir / "traces"
    logs_dir = company_dir / "logs"

    services = _extract_services_from_repo_defs(repos_dir)
    known_services = {s.name for s in services}

    repo_deps = _extract_dependencies_from_repo_defs(repos_dir)
    trace_deps = _extract_dependencies_from_traces(traces_dir)
    log_deps = _extract_dependencies_from_logs(logs_dir, known_services)

    all_deps = repo_deps + trace_deps + log_deps
    merged = merge_dependencies(all_deps)

    return services, merged