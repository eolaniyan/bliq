from pathlib import Path
from typing import Dict, List, Set
import re

from atlas_core.ingestion.file_loader import load_json_files_in_dir, load_text_files_in_dir
from atlas_core.normalization.service_name_resolver import normalize_service_name


def detect_drift(company_dir: Path) -> List[Dict]:
    repos_dir = company_dir / "repos"
    logs_dir = company_dir / "logs"
    traces_dir = company_dir / "traces"

    declared_edges: Set[tuple[str, str]] = set()
    observed_edges: Set[tuple[str, str]] = set()

    repo_files = load_json_files_in_dir(repos_dir)
    known_services = {normalize_service_name(item["service"]) for item in repo_files}

    for item in repo_files:
        source = normalize_service_name(item["service"])
        for target in item.get("calls", []):
            declared_edges.add((source, normalize_service_name(target)))

    logs = load_text_files_in_dir(logs_dir)
    call_pattern = re.compile(r"calling\s+([a-zA-Z0-9_\-]+)", re.IGNORECASE)

    for filename, content in logs.items():
        source = normalize_service_name(filename.replace(".log", ""))
        for line in content.splitlines():
            match = call_pattern.search(line)
            if match:
                target = normalize_service_name(match.group(1))
                if target in known_services:
                    observed_edges.add((source, target))

    trace_files = load_json_files_in_dir(traces_dir)
    for trace in trace_files:
        services = [normalize_service_name(s) for s in trace.get("services", [])]
        for i in range(len(services) - 1):
            source, target = services[i], services[i + 1]
            if source in known_services and target in known_services:
                observed_edges.add((source, target))

    drifts: List[Dict] = []

    runtime_only = observed_edges - declared_edges
    declared_only = declared_edges - observed_edges

    for source, target in sorted(runtime_only):
        drifts.append(
            {
                "type": "runtime_only",
                "source": source,
                "target": target,
                "message": f"Observed at runtime but not declared: {source} -> {target}",
                "severity": "warning",
            }
        )

    for source, target in sorted(declared_only):
        drifts.append(
            {
                "type": "declared_but_unobserved",
                "source": source,
                "target": target,
                "message": f"Declared in config but not seen in runtime signals: {source} -> {target}",
                "severity": "info",
            }
        )

    return drifts