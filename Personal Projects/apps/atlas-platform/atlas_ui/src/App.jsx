import { useEffect, useMemo, useState } from "react";
import {
  buildGraph,
  getCompanies,
  getDependencies,
  getDependents,
  getRunbook,
  getServices,
  simulateFailure,
  getDrift,
  getServiceIncidents,
} from "./api";
import CompanySelector from "./components/CompanySelector";
import ServiceList from "./components/ServiceList";
import GraphView from "./components/GraphView";
import ServiceDetails from "./components/ServiceDetails";
import GraphLegend from "./components/GraphLegend";
import IncidentPanel from "./components/IncidentPanel";
import DriftPanel from "./components/DriftPanel";

function inferDomain(serviceName) {
  if (
    serviceName.includes("auth") ||
    serviceName.includes("api_gateway") ||
    serviceName.includes("notification")
  ) return "platform";
  if (
    serviceName.includes("payment") ||
    serviceName.includes("checkout") ||
    serviceName.includes("merchant")
  ) return "payments";
  if (
    serviceName.includes("ledger") ||
    serviceName.includes("settlement") ||
    serviceName.includes("billing") ||
    serviceName.includes("invoice")
  ) return "finance";
  if (serviceName.includes("fraud")) return "risk";
  if (
    serviceName.includes("analytics") ||
    serviceName.includes("reporting")
  ) return "data";
  if (
    serviceName.includes("shipment") ||
    serviceName.includes("route") ||
    serviceName.includes("warehouse") ||
    serviceName.includes("tracking") ||
    serviceName.includes("fleet")
  ) return "operations";
  if (
    serviceName.includes("catalog") ||
    serviceName.includes("inventory") ||
    serviceName.includes("cart") ||
    serviceName.includes("order") ||
    serviceName.includes("shipping") ||
    serviceName.includes("recommendation")
  ) return "commerce";
  if (serviceName.includes("admin")) return "internal";

  return "core";
}

const GRAPH_MODE_INFO = {
  flow: {
    label: "Flow",
    description: "Best for following end-to-end request paths and business journeys.",
  },
  topology: {
    label: "Topology",
    description: "Best for exploring the overall dependency network and system connectivity.",
  },
  concentric: {
    label: "Concentric",
    description: "Best for highlighting central/shared services versus surrounding domain services.",
  },
};

function normalizeSearchValue(value) {
  return value
    .toLowerCase()
    .trim()
    .replace(/[_\-\s]+/g, "")
    .replace(/services/g, "service")
    .replace(/payments/g, "payment")
    .replace(/orders/g, "order")
    .replace(/shipments/g, "shipment")
    .replace(/notifications/g, "notification")
    .replace(/analytics/g, "analytic")
    .replace(/ies$/, "y")
    .replace(/s$/, "");
}

export default function App() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [buildResult, setBuildResult] = useState(null);

  const [services, setServices] = useState([]);
  const [graphEdges, setGraphEdges] = useState([]);
  const [selectedService, setSelectedService] = useState("");

  const [dependencies, setDependencies] = useState([]);
  const [dependents, setDependents] = useState([]);
  const [dependencyDetails, setDependencyDetails] = useState([]);
  const [dependentDetails, setDependentDetails] = useState([]);
  const [simulation, setSimulation] = useState(null);
  const [runbook, setRunbook] = useState(null);
  const [drifts, setDrifts] = useState([]);
  const [serviceIncidents, setServiceIncidents] = useState([]);

  const [tooltip, setTooltip] = useState(null);

  const [graphMode, setGraphMode] = useState("flow");
  const [graphFilter, setGraphFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [graphApi, setGraphApi] = useState(null);
  const [legendFilter, setLegendFilter] = useState(null);
  const [inspectorOpen, setInspectorOpen] = useState(false);

  const [loadingCompanies, setLoadingCompanies] = useState(false);
  const [buildingGraph, setBuildingGraph] = useState(false);
  const [loadingServiceData, setLoadingServiceData] = useState(false);
  const [loadingDrift, setLoadingDrift] = useState(false);
  const [loadingIncidents, setLoadingIncidents] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCompanies() {
      try {
        setLoadingCompanies(true);
        setError("");
        const data = await getCompanies();
        const items = data.companies || [];
        setCompanies(items);
        if (items.length > 0) {
          setSelectedCompany(items[0]);
        }
      } catch (err) {
        setError(`Failed to load companies: ${err.message}`);
      } finally {
        setLoadingCompanies(false);
      }
    }

    loadCompanies();
  }, []);

  async function handleBuildGraph() {
    if (!selectedCompany) return;

    try {
      setBuildingGraph(true);
      setError("");
      setSelectedService("");
      setDependencies([]);
      setDependents([]);
      setDependencyDetails([]);
      setDependentDetails([]);
      setSimulation(null);
      setRunbook(null);
      setGraphEdges([]);
      setDrifts([]);
      setServiceIncidents([]);
      setTooltip(null);
      setLegendFilter(null);
      setInspectorOpen(false);

      const result = await buildGraph(selectedCompany);
      setBuildResult(result);

      const servicesResponse = await getServices(selectedCompany);
      const serviceNames = servicesResponse.services || [];
      setServices(serviceNames);

      const edgeAccumulator = [];
      for (const serviceName of serviceNames) {
        const depResponse = await getDependencies(serviceName, selectedCompany);
        const depDetails = depResponse.dependency_details || [];

        for (const dep of depDetails) {
          edgeAccumulator.push({
            source: dep.source,
            target: dep.target,
            relationship: dep.relationship,
            confidence: dep.confidence,
            evidence_sources: dep.evidence_sources || [],
          });
        }
      }

      setGraphEdges(edgeAccumulator);

      setLoadingDrift(true);
      const driftResponse = await getDrift(selectedCompany);
      setDrifts(driftResponse.drifts || []);
      setLoadingDrift(false);

      if (serviceNames.length > 0) {
        setSelectedService(serviceNames[0]);
        setInspectorOpen(true);
      }
    } catch (err) {
      setError(`Failed to build graph: ${err.response?.data?.detail || err.message}`);
    } finally {
      setBuildingGraph(false);
    }
  }

  useEffect(() => {
    async function loadServiceData() {
      if (!selectedService || !selectedCompany) return;

      try {
        setLoadingServiceData(true);
        setLoadingIncidents(true);
        setError("");

        const [deps, dents, sim, rb, incidents] = await Promise.all([
          getDependencies(selectedService, selectedCompany),
          getDependents(selectedService, selectedCompany),
          simulateFailure(selectedService, selectedCompany),
          getRunbook(selectedService, selectedCompany),
          getServiceIncidents(selectedCompany, selectedService),
        ]);

        setDependencies(deps.dependencies || []);
        setDependents(dents.dependents || []);
        setDependencyDetails(deps.dependency_details || []);
        setDependentDetails(dents.dependent_details || []);
        setSimulation(sim);
        setRunbook(rb);
        setServiceIncidents(incidents.incidents || []);
      } catch (err) {
        setError(`Failed to load service data: ${err.response?.data?.detail || err.message}`);
      } finally {
        setLoadingServiceData(false);
        setLoadingIncidents(false);
      }
    }

    loadServiceData();
  }, [selectedService, selectedCompany]);

  function handleSearchFocus() {
    const normalizedInput = normalizeSearchValue(searchTerm);
    if (!normalizedInput) return;

    const match = services.find((svc) => {
      const normalizedService = normalizeSearchValue(svc);
      return (
        normalizedService.includes(normalizedInput) ||
        normalizedInput.includes(normalizedService)
      );
    });

    if (match) {
      setSelectedService(match);
      setInspectorOpen(true);
      graphApi?.focusNode?.(match);
    }
  }

  function handleSearchKeyDown(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSearchFocus();
    }
  }

  function handleLegendToggle(domainKey) {
    setLegendFilter((prev) => (prev === domainKey ? null : domainKey));
  }

  function handleSelectNode(nodeId) {
    setSelectedService(nodeId);
    setInspectorOpen(true);
  }

  const graphElements = useMemo(() => {
    const elements = [];
    const nodeSet = new Set();
    const edgeSet = new Set();

    const connectedNodes = new Set();
    if (selectedService) {
      connectedNodes.add(selectedService);
      dependencies.forEach((d) => connectedNodes.add(d));
      dependents.forEach((d) => connectedNodes.add(d));
    }

    const driftedNodes = new Set();
    drifts.forEach((d) => {
      driftedNodes.add(d.source);
      driftedNodes.add(d.target);
    });

    let servicesToRender =
      graphFilter === "connected" && selectedService
        ? services.filter((svc) => connectedNodes.has(svc))
        : services;

    if (legendFilter) {
      servicesToRender = servicesToRender.filter((svc) => inferDomain(svc) === legendFilter);
    }

    for (const svc of servicesToRender) {
      if (!nodeSet.has(svc)) {
        nodeSet.add(svc);

        const domain = inferDomain(svc);

        let kind = "service";
        if (svc === selectedService) kind = "selected";
        else if (simulation?.impacted_services?.includes(svc)) kind = "impacted";
        else if (driftedNodes.has(svc)) kind = "drifted";

        elements.push({
          data: {
            id: svc,
            label: svc,
            rawLabel: svc,
            kind,
            domain,
            muted: legendFilter && domain !== legendFilter ? "true" : "false",
          },
        });
      }
    }

    for (const edge of graphEdges) {
      if (graphFilter === "connected" && selectedService) {
        if (!connectedNodes.has(edge.source) || !connectedNodes.has(edge.target)) {
          continue;
        }
      }

      if (!nodeSet.has(edge.source) || !nodeSet.has(edge.target)) continue;

      const edgeId = `${edge.source}->${edge.target}`;
      if (!edgeSet.has(edgeId)) {
        edgeSet.add(edgeId);
        elements.push({
          data: {
            id: edgeId,
            source: edge.source,
            target: edge.target,
            relationship: edge.relationship,
            confidence: edge.confidence,
            evidence_sources: (edge.evidence_sources || []).join(", "),
          },
        });
      }
    }

    return elements;
  }, [
    services,
    graphEdges,
    selectedService,
    graphFilter,
    dependencies,
    dependents,
    simulation,
    drifts,
    legendFilter,
  ]);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h1>Atlas Platform Intelligence</h1>
          <p className="subtext">Synthetic enterprise platform explorer</p>
        </div>
      </header>

      <div className={`workspace ${inspectorOpen ? "inspector-open" : ""}`}>
        <aside className="sidebar">
          <CompanySelector
            companies={companies}
            selectedCompany={selectedCompany}
            setSelectedCompany={setSelectedCompany}
            onBuildGraph={handleBuildGraph}
            loadingCompanies={loadingCompanies}
            buildingGraph={buildingGraph}
            buildResult={buildResult}
          />

          <section className="panel">
            <div className="panel-header">
              <h2>Graph Controls</h2>
            </div>

            <div className="stack">
              <label className="label">Graph style</label>
              <select
                className="input"
                value={graphMode}
                onChange={(e) => setGraphMode(e.target.value)}
              >
                <option value="flow">Flow</option>
                <option value="topology">Topology</option>
                <option value="concentric">Concentric</option>
              </select>

              <div className="muted small graph-mode-help">
                <strong>{GRAPH_MODE_INFO[graphMode].label}:</strong> {GRAPH_MODE_INFO[graphMode].description}
              </div>

              <label className="label">Filter</label>
              <select
                className="input"
                value={graphFilter}
                onChange={(e) => setGraphFilter(e.target.value)}
              >
                <option value="all">All services</option>
                <option value="connected">Connected services</option>
              </select>

              <div className="muted small">
                “Connected services” shows the selected service plus its direct dependencies and dependents.
              </div>

              <label className="label">Search and focus</label>
              <div className="search-row">
                <input
                  className="input"
                  placeholder="Search service..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyDown={handleSearchKeyDown}
                />
                <button className="button primary compact-button" onClick={handleSearchFocus}>
                  Focus
                </button>
              </div>
            </div>
          </section>

          <GraphLegend
            activeDomain={legendFilter}
            onToggle={handleLegendToggle}
          />

          <ServiceList
            services={services}
            selectedService={selectedService}
            setSelectedService={handleSelectNode}
          />
        </aside>

        <main className="graph-column">
          {error ? <div className="error-banner">{error}</div> : null}

          <section className="panel graph-panel">
            <div className="panel-header">
              <h2>Architecture Graph</h2>
              <span className="muted">
                {selectedCompany ? `Company: ${selectedCompany}` : "No company selected"}
              </span>
            </div>

            <GraphView
              elements={graphElements}
              selectedService={selectedService}
              graphMode={graphMode}
              onSelectNode={handleSelectNode}
              onTooltipChange={setTooltip}
              onApiReady={setGraphApi}
            />

            {tooltip ? (
              <div
                className="graph-tooltip"
                style={{
                  left: tooltip.x,
                  top: tooltip.y,
                }}
              >
                {tooltip.type === "node" ? (
                  <>
                    <div><strong>{tooltip.label}</strong></div>
                    <div className="muted small">Domain: {tooltip.domain}</div>
                    <div className="muted small">State: {tooltip.kind}</div>
                  </>
                ) : (
                  <>
                    <div><strong>{tooltip.source} → {tooltip.target}</strong></div>
                    <div className="muted small">Relationship: {tooltip.relationship}</div>
                    <div className="muted small">Confidence: {tooltip.confidence}</div>
                    <div className="muted small">Evidence: {tooltip.evidence_sources || "None"}</div>
                  </>
                )}
              </div>
            ) : null}
          </section>
        </main>

        {inspectorOpen ? (
          <aside className="inspector-panel">
            <div className="panel inspector-inner">
              <div className="panel-header">
                <h2>Service Inspector</h2>
                <button
                  className="button export-button compact-button"
                  onClick={() => setInspectorOpen(false)}
                >
                  Close
                </button>
              </div>

              <ServiceDetails
                selectedService={selectedService}
                dependencies={dependencies}
                dependents={dependents}
                dependencyDetails={dependencyDetails}
                dependentDetails={dependentDetails}
                simulation={simulation}
                runbook={runbook}
                loading={loadingServiceData}
                serviceIncidents={serviceIncidents}
              />

              <DriftPanel drifts={drifts} loading={loadingDrift} />
              <IncidentPanel
                incidents={serviceIncidents}
                loading={loadingIncidents}
                selectedService={selectedService}
              />
            </div>
          </aside>
        ) : null}
      </div>
    </div>
  );
}