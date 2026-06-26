from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from atlas_core.config import DATA_ROOT
from atlas_core.graph.graph_queries import GRAPH_STORE
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


def _resolve_company_dir(company: str) -> Path:
    if not company or company in {".", ".."} or company != Path(company).name or "\\" in company:
        raise HTTPException(status_code=404, detail=f"Company '{company}' not found.")

    data_root = DATA_ROOT.resolve()
    company_dir = (data_root / company).resolve()

    if company_dir.parent != data_root or not company_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"Company '{company}' not found.")

    return company_dir


@app.get("/")
def root() -> dict:
    return {
        "message": "Atlas Platform Intelligence MVP is running",
        "data_root": str(DATA_ROOT),
    }


@app.get("/companies")
def list_companies() -> dict:
    if not DATA_ROOT.is_dir():
        return {"companies": []}

    companies = sorted([p.name for p in DATA_ROOT.iterdir() if p.is_dir()])
    return {"companies": companies}


@app.post("/graph/build", response_model=BuildGraphResponse)
def build_graph(company: str) -> BuildGraphResponse:
    company_dir = _resolve_company_dir(company)

    services, deps = infer_company_graph(company_dir)

    GRAPH_STORE.clear()
    GRAPH_STORE.company_name = company

    for service in services:
        GRAPH_STORE.add_service(service)

    for dep in deps:
        GRAPH_STORE.add_dependency(dep)

    return BuildGraphResponse(
        company=company,
        services_detected=GRAPH_STORE.node_count(),
        dependencies_detected=GRAPH_STORE.edge_count(),
        message="Architecture graph built successfully.",
    )


@app.get("/graph/services")
def get_services() -> dict:
    return {
        "company": GRAPH_STORE.company_name,
        "services": GRAPH_STORE.get_services(),
    }


@app.get("/graph/dependencies/{service_name}")
def get_dependencies(service_name: str) -> dict:
    return {
        "service": service_name,
        "dependencies": GRAPH_STORE.get_dependencies(service_name),
        "dependency_details": GRAPH_STORE.get_dependency_details(service_name),
    }


@app.get("/graph/dependents/{service_name}")
def get_dependents(service_name: str) -> dict:
    return {
        "service": service_name,
        "dependents": GRAPH_STORE.get_dependents(service_name),
        "dependent_details": GRAPH_STORE.get_dependent_details(service_name),
    }


@app.get("/graph/simulate/{service_name}", response_model=BlastRadiusResponse)
def simulate_service_failure(service_name: str) -> BlastRadiusResponse:
    if service_name not in GRAPH_STORE.graph:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found in graph.")

    direct_dependents, impacted_services = simulate_failure(GRAPH_STORE, service_name)

    return BlastRadiusResponse(
        failed_service=service_name,
        direct_dependents=direct_dependents,
        impacted_services=impacted_services,
        notes="This is a simple graph-based simulation for MVP purposes.",
    )


@app.get("/graph/runbook/{service_name}", response_model=RunbookResponse)
def get_runbook(service_name: str) -> RunbookResponse:
    if service_name not in GRAPH_STORE.graph:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found in graph.")

    checks = generate_runbook(GRAPH_STORE, service_name)
    return RunbookResponse(
        service=service_name,
        checks=checks,
        notes="Generated from graph relationships and basic rule logic.",
    )


@app.get("/graph/drift")
def get_graph_drift(company: str) -> dict:
    company_dir = _resolve_company_dir(company)

    drifts = detect_drift(company_dir)
    return {
        "company": company,
        "drifts": drifts,
        "count": len(drifts),
    }


@app.get("/incidents")
def get_company_incidents(company: str) -> dict:
    company_dir = _resolve_company_dir(company)

    incidents = load_incidents(company_dir)
    return {
        "company": company,
        "incidents": incidents,
        "count": len(incidents),
    }


@app.get("/incidents/{service_name}")
def get_service_incidents(service_name: str, company: str) -> dict:
    company_dir = _resolve_company_dir(company)

    incidents = load_incidents_for_service(company_dir, service_name)
    return {
        "company": company,
        "service": service_name,
        "incidents": incidents,
        "count": len(incidents),
    }