from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class ServiceDependency(BaseModel):
    source: str
    target: str
    relationship: str = "CALLS"
    confidence: float = 0.5
    evidence_sources: List[str] = Field(default_factory=list)


class ServiceNode(BaseModel):
    name: str
    service_type: str = "service"
    metadata: Dict[str, str] = Field(default_factory=dict)


class BuildGraphResponse(BaseModel):
    company: str
    services_detected: int
    dependencies_detected: int
    message: str


class BlastRadiusResponse(BaseModel):
    failed_service: str
    impacted_services: List[str]
    direct_dependents: List[str]
    notes: Optional[str] = None


class RunbookResponse(BaseModel):
    service: str
    checks: List[str]
    notes: str