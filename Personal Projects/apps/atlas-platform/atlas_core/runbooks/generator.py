from atlas_core.graph.graph_builder import AtlasGraphStore


def generate_runbook(graph_store: AtlasGraphStore, service_name: str) -> list[str]:
    deps = graph_store.get_dependencies(service_name)
    dependents = graph_store.get_dependents(service_name)

    checks = [
        f"Confirm whether {service_name} is reachable and healthy.",
        f"Check recent logs for {service_name}.",
        f"Check whether there was a recent deployment for {service_name}.",
    ]

    if deps:
        checks.append(f"Validate downstream dependencies: {', '.join(deps)}.")

    if dependents:
        checks.append(f"Check upstream callers affected by this issue: {', '.join(dependents)}.")

    checks.append("Review timeout, error rate, and latency patterns.")
    checks.append("Check for configuration drift or undocumented dependency changes.")

    return checks