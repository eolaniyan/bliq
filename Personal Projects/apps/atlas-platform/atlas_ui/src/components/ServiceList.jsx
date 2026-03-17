export default function ServiceList({ services, selectedService, setSelectedService }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Services</h2>
      </div>

      <div className="service-list">
        {services.length === 0 ? (
          <div className="muted small">No services loaded yet.</div>
        ) : (
          services.map((service) => (
            <button
              key={service}
              className={`service-item ${selectedService === service ? "active" : ""}`}
              onClick={() => setSelectedService(service)}
            >
              {service}
            </button>
          ))
        )}
      </div>
    </section>
  );
}