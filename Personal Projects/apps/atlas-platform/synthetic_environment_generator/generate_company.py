import json
import sys
from pathlib import Path
from faker import Faker

fake = Faker()

BASE_DIR = Path(__file__).resolve().parent.parent
COMPANIES_DIR = BASE_DIR / "synthetic_companies"


ARCHITECTURES = {
    "novapay_fintech": {
        "company": "NovaPay",
        "industry": "fintech",
        "services": [
            "api_gateway",
            "auth_service",
            "merchant_service",
            "checkout_service",
            "payment_service",
            "fraud_service",
            "ledger_service",
            "settlement_service",
            "reporting_service",
            "notification_service",
            "analytics_service",
            "admin_portal",
        ],
        "domains": {
            "api_gateway": "platform",
            "auth_service": "platform",
            "merchant_service": "merchant",
            "checkout_service": "payments",
            "payment_service": "payments",
            "fraud_service": "risk",
            "ledger_service": "finance",
            "settlement_service": "finance",
            "reporting_service": "reporting",
            "notification_service": "platform",
            "analytics_service": "data",
            "admin_portal": "internal",
        },
        "edges": [
            ("api_gateway", "auth_service"),
            ("api_gateway", "checkout_service"),
            ("api_gateway", "merchant_service"),
            ("checkout_service", "payment_service"),
            ("checkout_service", "notification_service"),
            ("payment_service", "ledger_service"),
            ("ledger_service", "settlement_service"),
            ("settlement_service", "reporting_service"),
            ("merchant_service", "reporting_service"),
            ("analytics_service", "reporting_service"),
            ("admin_portal", "merchant_service"),
            ("admin_portal", "reporting_service"),
            ("admin_portal", "analytics_service"),
            ("notification_service", "analytics_service"),
            ("payment_service", "reporting_service")
        ],
        "runtime_only_edges": [
            ("payment_service", "fraud_service"),
        ],
        "trace_flows": [
            ["api_gateway", "auth_service"],
            ["api_gateway", "checkout_service", "payment_service", "fraud_service"],
            ["api_gateway", "checkout_service", "payment_service", "ledger_service", "settlement_service"],
            ["admin_portal", "merchant_service", "reporting_service"],
            ["admin_portal", "analytics_service", "reporting_service"],
        ],
        "incidents": [
            {
                "incident_id": "INC-001",
                "service": "fraud_service",
                "severity": "high",
                "title": "Fraud scoring latency spike",
                "impact": "payment authorization latency increased and checkout success rate dropped",
                "resolution": "scaled fraud workers and cleared pending risk evaluations",
            },
            {
                "incident_id": "INC-002",
                "service": "settlement_service",
                "severity": "medium",
                "title": "Settlement batch processing delay",
                "impact": "merchant payouts and reconciliation reports delayed",
                "resolution": "restarted settlement workers and replayed batch queue",
            },
        ],
    },
    "shopsphere_ecommerce": {
        "company": "ShopSphere",
        "industry": "ecommerce",
        "services": [
            "api_gateway",
            "auth_service",
            "product_catalog_service",
            "inventory_service",
            "cart_service",
            "checkout_service",
            "payment_service",
            "order_service",
            "shipping_service",
            "recommendation_service",
            "notification_service",
            "analytics_service",
        ],
        "domains": {
            "api_gateway": "platform",
            "auth_service": "platform",
            "product_catalog_service": "catalog",
            "inventory_service": "catalog",
            "cart_service": "commerce",
            "checkout_service": "commerce",
            "payment_service": "payments",
            "order_service": "orders",
            "shipping_service": "fulfillment",
            "recommendation_service": "personalization",
            "notification_service": "platform",
            "analytics_service": "data",
        },
        "edges": [
            ("api_gateway", "auth_service"),
            ("api_gateway", "product_catalog_service"),
            ("api_gateway", "cart_service"),
            ("api_gateway", "checkout_service"),
            ("product_catalog_service", "inventory_service"),
            ("cart_service", "product_catalog_service"),
            ("cart_service", "inventory_service"),
            ("checkout_service", "cart_service"),
            ("checkout_service", "payment_service"),
            ("payment_service", "order_service"),
            ("order_service", "inventory_service"),
            ("order_service", "shipping_service"),
            ("order_service", "notification_service"),
            ("recommendation_service", "product_catalog_service"),
            ("analytics_service", "order_service"),
            ("analytics_service", "shipping_service"),
            ("notification_service", "analytics_service"),
            ("order_service", "recommendation_service"),
        ],
        "runtime_only_edges": [
            ("checkout_service", "inventory_service"),
        ],
        "trace_flows": [
            ["api_gateway", "auth_service"],
            ["api_gateway", "product_catalog_service", "inventory_service"],
            ["api_gateway", "cart_service", "product_catalog_service"],
            ["api_gateway", "checkout_service", "payment_service", "order_service", "shipping_service"],
            ["order_service", "notification_service", "analytics_service"],
        ],
        "incidents": [
            {
                "incident_id": "INC-001",
                "service": "inventory_service",
                "severity": "high",
                "title": "Inventory service outage",
                "impact": "checkout confirmation failed for in-stock validation",
                "resolution": "restarted inventory cluster and restored product stock cache",
            },
            {
                "incident_id": "INC-002",
                "service": "shipping_service",
                "severity": "medium",
                "title": "Carrier integration latency",
                "impact": "shipment creation delayed and order notifications lagged",
                "resolution": "failed over carrier adapter and retried queued shipments",
            },
        ],
    },
    "routeflow_logistics": {
        "company": "RouteFlow",
        "industry": "logistics",
        "services": [
            "api_gateway",
            "auth_service",
            "shipment_service",
            "route_planning_service",
            "warehouse_service",
            "tracking_service",
            "fleet_management_service",
            "billing_service",
            "invoice_service",
            "notification_service",
            "analytics_service",
            "admin_portal",
        ],
        "domains": {
            "api_gateway": "platform",
            "auth_service": "platform",
            "shipment_service": "operations",
            "route_planning_service": "operations",
            "warehouse_service": "operations",
            "tracking_service": "operations",
            "fleet_management_service": "fleet",
            "billing_service": "finance",
            "invoice_service": "finance",
            "notification_service": "platform",
            "analytics_service": "data",
            "admin_portal": "internal",
        },
        "edges": [
            ("api_gateway", "auth_service"),
            ("api_gateway", "shipment_service"),
            ("api_gateway", "tracking_service"),
            ("shipment_service", "route_planning_service"),
            ("shipment_service", "tracking_service"),
            ("route_planning_service", "fleet_management_service"),
            ("warehouse_service", "tracking_service"),
            ("tracking_service", "notification_service"),
            ("tracking_service", "analytics_service"),
            ("shipment_service", "billing_service"),
            ("billing_service", "invoice_service"),
            ("admin_portal", "analytics_service"),
            ("admin_portal", "shipment_service"),
            ("admin_portal", "billing_service"),
            ("route_planning_service", "analytics_service"),
        ],
        "runtime_only_edges": [
            ("shipment_service", "warehouse_service"),
        ],
        "trace_flows": [
            ["api_gateway", "auth_service"],
            ["api_gateway", "shipment_service", "route_planning_service", "fleet_management_service"],
            ["api_gateway", "shipment_service", "warehouse_service", "tracking_service"],
            ["shipment_service", "billing_service", "invoice_service"],
            ["tracking_service", "notification_service", "analytics_service"],
            ["admin_portal", "analytics_service"],
        ],
        "incidents": [
            {
                "incident_id": "INC-001",
                "service": "route_planning_service",
                "severity": "high",
                "title": "Route optimization service degradation",
                "impact": "shipment scheduling slowed and fleet allocation delays increased",
                "resolution": "scaled route workers and flushed optimization backlog",
            },
            {
                "incident_id": "INC-002",
                "service": "tracking_service",
                "severity": "medium",
                "title": "Tracking event backlog",
                "impact": "status updates and outbound notifications delayed",
                "resolution": "restarted event consumers and replayed tracking stream",
            },
        ],
    },
}


def ensure_dirs(company_dir: Path) -> None:
    for sub in ["repos", "logs", "traces", "incidents", "docs"]:
        (company_dir / sub).mkdir(parents=True, exist_ok=True)


def clear_existing(company_dir: Path) -> None:
    if not company_dir.exists():
        return
    for sub in ["repos", "logs", "traces", "incidents", "docs"]:
        subdir = company_dir / sub
        if subdir.exists():
            for path in subdir.iterdir():
                if path.is_file():
                    path.unlink()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def service_calls_for(service_name: str, edges: list[tuple[str, str]]) -> list[str]:
    return [target for source, target in edges if source == service_name]


def generate_repos(company_dir: Path, config: dict) -> None:
    edges = config["edges"]
    domains = config["domains"]

    for service in config["services"]:
        payload = {
            "service": service,
            "repo": f"{service}_repo",
            "calls": service_calls_for(service, edges),
            "domain": domains.get(service, "core"),
        }
        write_json(company_dir / "repos" / f"{service}.json", payload)


def generate_traces(company_dir: Path, config: dict) -> None:
    flow_index = 1
    for flow in config["trace_flows"]:
        for _ in range(8):
            payload = {
                "trace_id": f"trace_{flow_index:04d}",
                "services": flow,
            }
            write_json(company_dir / "traces" / f"trace_{flow_index:04d}.json", payload)
            flow_index += 1


def generate_logs(company_dir: Path, config: dict) -> None:
    declared_edges = config["edges"]
    runtime_only_edges = config.get("runtime_only_edges", [])
    all_runtime_edges = [*declared_edges, *runtime_only_edges]
    service_calls = {svc: service_calls_for(svc, all_runtime_edges) for svc in config["services"]}

    for service in config["services"]:
        lines: list[str] = []
        calls = service_calls.get(service, [])

        for i in range(120):
            ts = fake.iso8601()

            if calls:
                target = calls[i % len(calls)]
                if i % 17 == 0:
                    lines.append(f"{ts} {service} WARN request to {target} slower than threshold")
                elif i % 41 == 0:
                    lines.append(f"{ts} {service} ERROR timeout detected while calling {target}")
                else:
                    lines.append(f"{ts} {service} INFO calling {target}")
            else:
                if i % 29 == 0:
                    lines.append(f"{ts} {service} WARN worker cycle delayed")
                else:
                    lines.append(f"{ts} {service} INFO request processed")

        if service == "payment_service":
            lines.append(f"{fake.iso8601()} payment_service INFO calling fraud-service")
            lines.append(f"{fake.iso8601()} payment_service INFO calling ledger-service")

        (company_dir / "logs" / f"{service}.log").write_text("\n".join(lines), encoding="utf-8")


def generate_incidents(company_dir: Path, config: dict) -> None:
    for incident in config["incidents"]:
        write_json(company_dir / "incidents" / f"{incident['incident_id']}.json", incident)


def generate_docs(company_dir: Path, config: dict) -> None:
    services = config["services"]
    edges = config["edges"]

    overview = [
        f"# {config['company']} Architecture Overview",
        "",
        f"Industry: {config['industry']}",
        "",
        "Core services:",
    ]
    overview.extend([f"- {svc}" for svc in services[:8]])
    overview.extend(
        [
            "",
            "Known declared relationships:",
            *[f"- {src} -> {dst}" for src, dst in edges[:10]],
            "",
            "Note: runtime architecture may contain additional observed relationships.",
        ]
    )

    (company_dir / "docs" / "architecture_overview.md").write_text(
        "\n".join(overview), encoding="utf-8"
    )

    for service in services[:3]:
        doc = [
            f"# {service}",
            "",
            f"{service} is part of the {config['industry']} platform.",
            "",
            "Dependencies documented here may lag behind runtime behavior.",
        ]
        (company_dir / "docs" / f"{service}.md").write_text("\n".join(doc), encoding="utf-8")


def generate_company(template_name: str) -> None:
    if template_name not in ARCHITECTURES:
        raise ValueError(f"Unknown company template: {template_name}")

    config = ARCHITECTURES[template_name]
    company_dir = COMPANIES_DIR / template_name

    ensure_dirs(company_dir)
    clear_existing(company_dir)

    generate_repos(company_dir, config)
    generate_traces(company_dir, config)
    generate_logs(company_dir, config)
    generate_incidents(company_dir, config)
    generate_docs(company_dir, config)

    print(f"Generated synthetic company: {template_name}")


def generate_all() -> None:
    for template_name in ARCHITECTURES.keys():
        generate_company(template_name)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        generate_all()
    else:
        generate_company(sys.argv[1])