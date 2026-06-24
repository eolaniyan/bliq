export default function GraphLegend({ activeDomain, onToggle }) {
  const items = [
    { label: "Platform", cls: "legend-dot platform", key: "platform" },
    { label: "Payments", cls: "legend-dot payments", key: "payments" },
    { label: "Finance", cls: "legend-dot finance", key: "finance" },
    { label: "Risk", cls: "legend-dot risk", key: "risk" },
    { label: "Data", cls: "legend-dot data", key: "data" },
    { label: "Operations", cls: "legend-dot operations", key: "operations" },
    { label: "Commerce", cls: "legend-dot commerce", key: "commerce" },
    { label: "Internal", cls: "legend-dot internal", key: "internal" },
  ];

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Legend</h2>
      </div>

      <div className="legend-grid">
        {items.map((item) => (
          <button
            type="button"
            className={`legend-button ${activeDomain === item.key ? "active" : ""}`}
            key={item.label}
            onClick={() => onToggle(item.key)}
          >
            <span className={item.cls}></span>
            <span>{item.label}</span>
          </button>
        ))}
      </div>

      <div className="muted small">
        Click a legend item to highlight that domain. Click it again to clear.
      </div>
    </section>
  );
}