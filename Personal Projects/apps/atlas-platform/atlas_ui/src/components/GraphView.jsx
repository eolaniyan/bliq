import { useEffect, useRef } from "react";
import CytoscapeComponent from "react-cytoscapejs";

function getLayout(graphMode) {
  if (graphMode === "topology") {
    return {
      name: "cose",
      animate: true,
      fit: true,
      padding: 50,
      randomize: true,
      componentSpacing: 120,
      nodeRepulsion: 400000,
      nodeOverlap: 20,
      idealEdgeLength: 120,
      edgeElasticity: 100,
      nestingFactor: 1.2,
      gravity: 0.25,
      numIter: 2500,
      initialTemp: 1000,
      coolingFactor: 0.95,
      minTemp: 1.0,
    };
  }

  if (graphMode === "concentric") {
    return {
      name: "concentric",
      fit: true,
      padding: 50,
      animate: true,
      minNodeSpacing: 40,
      concentric: function (node) {
        const domain = node.data("domain");
        const kind = node.data("kind");
        if (kind === "selected") return 100;
        if (domain === "platform") return 80;
        if (domain === "payments" || domain === "operations" || domain === "commerce") return 60;
        if (domain === "finance" || domain === "risk" || domain === "data") return 40;
        return 20;
      },
      levelWidth: () => 20,
    };
  }

  return {
    name: "breadthfirst",
    fit: true,
    directed: true,
    padding: 50,
    spacingFactor: 1.3,
    animate: true,
  };
}

export default function GraphView({
  elements,
  selectedService,
  graphMode,
  onSelectNode,
  onTooltipChange,
  onApiReady,
}) {
  const cyRef = useRef(null);

  const stylesheet = [
    {
      selector: "node",
      style: {
        label: "data(label)",
        "text-wrap": "wrap",
        "text-max-width": 140,
        "font-size": 10,
        "text-valign": "center",
        "text-halign": "center",
        width: 44,
        height: 44,
        color: "#f8fafc",
        "background-color": "#475569",
        "border-width": 1.5,
        "border-color": "rgba(255,255,255,0.08)",
        shape: "round-rectangle",
      },
    },
    {
      selector: 'node[domain = "platform"]',
      style: { "background-color": "#3b82f6" },
    },
    {
      selector: 'node[domain = "payments"]',
      style: { "background-color": "#10b981" },
    },
    {
      selector: 'node[domain = "finance"]',
      style: { "background-color": "#14b8a6" },
    },
    {
      selector: 'node[domain = "risk"]',
      style: { "background-color": "#ef4444" },
    },
    {
      selector: 'node[domain = "data"]',
      style: { "background-color": "#8b5cf6" },
    },
    {
      selector: 'node[domain = "operations"]',
      style: { "background-color": "#f97316" },
    },
    {
      selector: 'node[domain = "commerce"]',
      style: { "background-color": "#22c55e" },
    },
    {
      selector: 'node[domain = "internal"]',
      style: { "background-color": "#eab308" },
    },
    {
      selector: 'node[kind = "selected"]',
      style: {
        width: 58,
        height: 58,
        "font-size": 11,
        "border-width": 4,
        "border-color": "#f8fafc",
      },
    },
    {
      selector: 'node[kind = "impacted"]',
      style: {
        "border-width": 3,
        "border-color": "#fb7185",
      },
    },
    {
      selector: 'node[kind = "drifted"]',
      style: {
        "border-width": 3,
        "border-color": "#f97316",
        "border-style": "dashed",
      },
    },
    {
      selector: 'node[muted = "true"]',
      style: {
        opacity: 0.22,
      },
    },
    {
      selector: "edge",
      style: {
        width: 2,
        "line-color": "rgba(148, 163, 184, 0.65)",
        "target-arrow-color": "rgba(148, 163, 184, 0.65)",
        "target-arrow-shape": "triangle",
        "curve-style": "bezier",
        opacity: 0.82,
      },
    },
  ];

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy || !elements || elements.length === 0) return;

    const layout = cy.layout(getLayout(graphMode));
    layout.run();

    setTimeout(() => {
      cy.fit(undefined, 40);
      cy.center();
    }, 500);
  }, [elements, graphMode, selectedService]);

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy || !onApiReady) return;

    onApiReady({
      resetLayout: () => {
        const layout = cy.layout(getLayout(graphMode));
        layout.run();
      },
      fitGraph: () => {
        cy.fit(undefined, 40);
        cy.center();
      },
      focusNode: (nodeId) => {
        const node = cy.getElementById(nodeId);
        if (node && node.length > 0) {
          cy.animate({
            center: { eles: node },
            zoom: 1.2,
            duration: 500,
          });
        }
      },
    });
  }, [graphMode, onApiReady]);

  function handleExport() {
    const cy = cyRef.current;
    if (!cy) return;

    const png = cy.png({
      full: true,
      scale: 2,
      bg: "#020617",
    });

    const link = document.createElement("a");
    link.href = png;
    link.download = "atlas-graph.png";
    link.click();
  }

  return (
    <>
      <div className="graph-toolbar">
        <button className="button export-button" onClick={handleExport}>
          Export PNG
        </button>
        <button
          className="button export-button"
          onClick={() => {
            const cy = cyRef.current;
            if (!cy) return;
            const layout = cy.layout(getLayout(graphMode));
            layout.run();
          }}
        >
          Reset Layout
        </button>
        <button
          className="button export-button"
          onClick={() => {
            const cy = cyRef.current;
            if (!cy) return;
            cy.fit(undefined, 40);
            cy.center();
          }}
        >
          Fit to Screen
        </button>
      </div>

      <div className="graph-wrap">
        <CytoscapeComponent
          elements={elements}
          style={{ width: "100%", height: "100%" }}
          stylesheet={stylesheet}
          cy={(cy) => {
            cyRef.current = cy;

            cy.removeAllListeners();

            cy.on("tap", "node", (evt) => {
              const node = evt.target;
              onSelectNode(node.id());
            });

            cy.on("mousemove", "node", (evt) => {
              const node = evt.target;
              const pos = evt.renderedPosition || { x: 0, y: 0 };
              onTooltipChange?.({
                type: "node",
                x: pos.x + 22,
                y: pos.y + 22,
                label: node.data("rawLabel"),
                domain: node.data("domain"),
                kind: node.data("kind"),
              });
            });

            cy.on("mousemove", "edge", (evt) => {
              const edge = evt.target;
              const pos = evt.renderedPosition || { x: 0, y: 0 };
              onTooltipChange?.({
                type: "edge",
                x: pos.x + 22,
                y: pos.y + 22,
                source: edge.data("source"),
                target: edge.data("target"),
                relationship: edge.data("relationship"),
                confidence: edge.data("confidence"),
                evidence_sources: edge.data("evidence_sources"),
              });
            });

            cy.on("mouseout", () => {
              onTooltipChange?.(null);
            });
          }}
        />
      </div>
    </>
  );
}