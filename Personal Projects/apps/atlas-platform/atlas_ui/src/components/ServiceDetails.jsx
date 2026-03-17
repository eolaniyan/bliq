function confidenceLabel(value) {
  if (value >= 0.9) return "High";
  if (value >= 0.75) return "Medium";
  return "Low";
}

export default function ServiceDetails({
  selectedService,
  dependencies,
  dependents,
  dependencyDetails,
  dependentDetails,
  simulation,
  runbook,
  loading,
  serviceIncidents,
}) {
  return (
    <div className="stack">
      {!selectedService ? (
        <div className="muted small">Click a node to inspect it in detail.</div>
      ) : (
        <>
          <div className="summary-card">
            <div><strong>Service:</strong> {selectedService}</div>
            <div><strong>Dependencies:</strong> {dependencies.length}</div>
            <div><strong>Dependents:</strong> {dependents.length}</div>
            <div><strong>Incidents:</strong> {serviceIncidents?.length || 0}</div>
          </div>

          <div>
            <div className="section-title">Downstream Dependencies</div>
            {dependencyDetails.length === 0 ? (
              <div className="muted small">No downstream dependencies found.</div>
            ) : (
              <div className="stack">
                {dependencyDetails.map((item, idx) => (
                  <div className="edge-card" key={`${item.source}-${item.target}-${idx}`}>
                    <div><strong>{item.source}</strong> → <strong>{item.target}</strong></div>
                    <div className="muted small">
                      {item.relationship} · Confidence: {confidenceLabel(item.confidence)} ({item.confidence})
                    </div>
                    <div className="muted small">
                      Evidence: {(item.evidence_sources || []).join(", ") || "None"}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div>
            <div className="section-title">Upstream Dependents</div>
            {dependentDetails.length === 0 ? (
              <div className="muted small">No upstream dependents found.</div>
            ) : (
              <div className="stack">
                {dependentDetails.map((item, idx) => (
                  <div className="edge-card" key={`${item.source}-${item.target}-${idx}`}>
                    <div><strong>{item.source}</strong> → <strong>{item.target}</strong></div>
                    <div className="muted small">
                      {item.relationship} · Confidence: {confidenceLabel(item.confidence)} ({item.confidence})
                    </div>
                    <div className="muted small">
                      Evidence: {(item.evidence_sources || []).join(", ") || "None"}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div>
            <div className="section-title">Operational Impact</div>
            {loading ? (
              <div className="muted small">Loading operational data...</div>
            ) : (
              <div className="stack">
                {simulation ? (
                  <div className="summary-card">
                    <div><strong>Blast radius:</strong> {simulation.impacted_services?.length || 0} impacted</div>
                    <div><strong>Direct dependents:</strong> {simulation.direct_dependents?.length || 0}</div>
                  </div>
                ) : null}

                <div>
                  <div className="section-title">Impacted Services</div>
                  {simulation?.impacted_services?.length ? (
                    <ul className="pill-list">
                      {simulation.impacted_services.map((item) => (
                        <li key={item} className="pill red">{item}</li>
                      ))}
                    </ul>
                  ) : (
                    <div className="muted small">No impacted services detected.</div>
                  )}
                </div>

                <div>
                  <div className="section-title">Runbook</div>
                  {runbook?.checks?.length ? (
                    <ol className="check-list">
                      {runbook.checks.map((check, index) => (
                        <li key={`${runbook.service}-${index}`}>{check}</li>
                      ))}
                    </ol>
                  ) : (
                    <div className="muted small">No runbook data available.</div>
                  )}
                </div>

                {runbook?.notes ? <div className="muted small">{runbook.notes}</div> : null}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}