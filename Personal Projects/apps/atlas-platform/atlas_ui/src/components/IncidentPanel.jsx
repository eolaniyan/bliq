export default function IncidentPanel({ incidents, loading, selectedService }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Incident History</h2>
      </div>

      {loading ? (
        <div className="muted small">Loading incidents...</div>
      ) : incidents.length === 0 ? (
        <div className="muted small">
          {selectedService
            ? `No incidents found for ${selectedService}.`
            : "No incidents found."}
        </div>
      ) : (
        <div className="incident-list">
          {incidents.map((incident) => (
            <div key={incident.incident_id} className="incident-card">
              <div className="incident-top">
                <strong>{incident.title}</strong>
                <span className={`severity-badge ${incident.severity}`}>
                  {incident.severity}
                </span>
              </div>
              <div className="muted small">
                <strong>ID:</strong> {incident.incident_id}
              </div>
              <div className="muted small">
                <strong>Service:</strong> {incident.service}
              </div>
              <div className="incident-section">
                <strong>Impact:</strong> {incident.impact}
              </div>
              <div className="incident-section">
                <strong>Resolution:</strong> {incident.resolution}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}