from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from atlas_core.config import DATA_ROOT
from atlas_core.graph.graph_builder import AtlasGraphStore
from atlas_core.graph.graph_queries import GRAPH_REGISTRY
from atlas_core.inference.dependency_inference import infer_company_graph
from atlas_core.inference.drift_detector import detect_drift
from atlas_core.incidents.service import load_incidents, load_incidents_for_service
from atlas_core.models import (
    BlastRadiusResponse,
    BuildGraphResponse,
    RunbookResponse,
)
from atlas_core.runbooks.generator import generate_runbook
from atlas_core.simulation.blast_radius import simulate_failure

app = FastAPI(title="Atlas Platform Intelligence MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_company_dir(company: str):
    data_root = DATA_ROOT.resolve()
    company_dir = (DATA_ROOT / company).resolve()

    if data_root != company_dir and data_root not in company_dir.parents:
        raise HTTPException(status_code=404, detail=f"Company '{company}' not found.")

    if not company_dir.exists() or not company_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"Company '{company}' not found.")

    return company_dir


def _build_graph_store(company: str) -> AtlasGraphStore:
    company_dir = _get_company_dir(company)
    services, deps = infer_company_graph(company_dir)

    graph_store = AtlasGraphStore()
    graph_store.company_name = company

    for service in services:
        graph_store.add_service(service)

    for dep in deps:
        graph_store.add_dependency(dep)

    return graph_store


def _get_graph_store(company: str | None) -> AtlasGraphStore | None:
    return GRAPH_REGISTRY.get_store(company)


@app.get("/")
def root() -> dict:
    return {
        "message": "Atlas Platform Intelligence MVP is running",
        "data_root": str(DATA_ROOT),
    }


@app.get("/companies")
def list_companies() -> dict:
    if not DATA_ROOT.exists():
        return {"companies": []}

    companies = sorted([p.name for p in DATA_ROOT.iterdir() if p.is_dir()])
    return {"companies": companies}


@app.post("/graph/build", response_model=BuildGraphResponse)
def build_graph(company: str) -> BuildGraphResponse:
    graph_store = _build_graph_store(company)
    GRAPH_REGISTRY.set_company_store(company, graph_store)

    return BuildGraphResponse(
        company=company,
        services_detected=graph_store.node_count(),
        dependencies_detected=graph_store.edge_count(),
        message="Architecture graph built successfully.",
    )


@app.get("/graph/services")
def get_services(company: str | None = None) -> dict:
    graph_store = _get_graph_store(company)

    return {
        "company": graph_store.company_name if graph_store else company,
        "services": graph_store.get_services() if graph_store else [],
    }


@app.get("/graph/dependencies/{service_name}")
def get_dependencies(service_name: str, company: str | None = None) -> dict:
    graph_store = _get_graph_store(company)

    return {
        "company": graph_store.company_name if graph_store else company,
        "service": service_name,
        "dependencies": graph_store.get_dependencies(service_name) if graph_store else [],
        "dependency_details": graph_store.get_dependency_details(service_name) if graph_store else [],
    }


@app.get("/graph/dependents/{service_name}")
def get_dependents(service_name: str, company: str | None = None) -> dict:
    graph_store = _get_graph_store(company)

    return {
        "company": graph_store.company_name if graph_store else company,
        "service": service_name,
        "dependents": graph_store.get_dependents(service_name) if graph_store else [],
        "dependent_details": graph_store.get_dependent_details(service_name) if graph_store else [],
    }


@app.get("/graph/simulate/{service_name}", response_model=BlastRadiusResponse)
def simulate_service_failure(service_name: str, company: str | None = None) -> BlastRadiusResponse:
    graph_store = _get_graph_store(company)
    if graph_store is None or service_name not in graph_store.graph:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found in graph.")

    direct_dependents, impacted_services = simulate_failure(graph_store, service_name)

    return BlastRadiusResponse(
        failed_service=service_name,
        direct_dependents=direct_dependents,
        impacted_services=impacted_services,
        notes="This is a simple graph-based simulation for MVP purposes.",
    )


@app.get("/graph/runbook/{service_name}", response_model=RunbookResponse)
def get_runbook(service_name: str, company: str | None = None) -> RunbookResponse:
    graph_store = _get_graph_store(company)
    if graph_store is None or service_name not in graph_store.graph:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found in graph.")

    checks = generate_runbook(graph_store, service_name)
    return RunbookResponse(
        service=service_name,
        checks=checks,
        notes="Generated from graph relationships and basic rule logic.",
    )


@app.get("/graph/drift")
def get_graph_drift(company: str) -> dict:
    company_dir = _get_company_dir(company)
    drifts = detect_drift(company_dir)
    return {
        "company": company,
        "drifts": drifts,
        "count": len(drifts),
    }


@app.get("/incidents")
def get_company_incidents(company: str) -> dict:
    company_dir = _get_company_dir(company)
    incidents = load_incidents(company_dir)
    return {
        "company": company,
        "incidents": incidents,
        "count": len(incidents),
    }


@app.get("/incidents/{service_name}")
def get_service_incidents(service_name: str, company: str) -> dict:
    company_dir = _get_company_dir(company)
    incidents = load_incidents_for_service(company_dir, service_name)
    return {
        "company": company,
        "service": service_name,
        "incidents": incidents,
        "count": len(incidents),
    }