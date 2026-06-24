from pathlib import Path
from typing import Dict, List

from atlas_core.ingestion.file_loader import load_json_files_in_dir
from atlas_core.normalization.service_name_resolver import normalize_service_name


def load_incidents(company_dir: Path) -> List[Dict]:
    incidents_dir = company_dir / "incidents"
    incidents = load_json_files_in_dir(incidents_dir)

    for incident in incidents:
        if "service" in incident:
            incident["service"] = normalize_service_name(incident["service"])

    return incidents


def load_incidents_for_service(company_dir: Path, service_name: str) -> List[Dict]:
    normalized = normalize_service_name(service_name)
    incidents = load_incidents(company_dir)
    return [incident for incident in incidents if incident.get("service") == normalized]