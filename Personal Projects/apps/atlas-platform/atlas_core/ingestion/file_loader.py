import json
from pathlib import Path
from typing import Any, Dict, List


def load_json_file(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_json_files_in_dir(directory: Path) -> List[Dict[str, Any]]:
    if not directory.exists():
        return []

    data: List[Dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        data.append(load_json_file(path))
    return data


def load_text_files_in_dir(directory: Path, pattern: str = "*.log") -> Dict[str, str]:
    results: Dict[str, str] = {}
    if not directory.exists():
        return results

    for path in sorted(directory.glob(pattern)):
        results[path.name] = path.read_text(encoding="utf-8")
    return results