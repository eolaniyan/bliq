export default function DriftPanel({ drifts, loading }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Drift Overlay</h2>
      </div>

      {loading ? (
        <div className="muted small">Loading drift data...</div>
      ) : drifts.length === 0 ? (
        <div className="muted small">No drift detected.</div>
      ) : (
        <div className="stack">
          <div className="summary-card">
            <div><strong>Drift findings:</strong> {drifts.length}</div>
          </div>

          <div className="drift-list">
            {drifts.map((item, idx) => (
              <div className="drift-card" key={`${item.source}-${item.target}-${idx}`}>
                <div className="drift-top">
                  <strong>{item.type}</strong>
                  <span className={`severity-badge ${item.severity}`}>{item.severity}</span>
                </div>
                <div className="muted small">
                  {item.source} → {item.target}
                </div>
                <div className="incident-section">{item.message}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}