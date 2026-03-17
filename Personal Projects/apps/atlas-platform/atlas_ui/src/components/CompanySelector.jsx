export default function CompanySelector({
  companies,
  selectedCompany,
  setSelectedCompany,
  onBuildGraph,
  loadingCompanies,
  buildingGraph,
  buildResult,
}) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Company</h2>
      </div>

      <div className="stack">
        <label className="label" htmlFor="company-select">
          Select synthetic company
        </label>

        <select
          id="company-select"
          className="input"
          value={selectedCompany}
          onChange={(e) => setSelectedCompany(e.target.value)}
          disabled={loadingCompanies || companies.length === 0}
        >
          {companies.map((company) => (
            <option key={company} value={company}>
              {company}
            </option>
          ))}
        </select>

        <button className="button primary" onClick={onBuildGraph} disabled={!selectedCompany || buildingGraph}>
          {buildingGraph ? "Building..." : "Build Graph"}
        </button>

        {buildResult ? (
          <div className="summary-card">
            <div><strong>Company:</strong> {buildResult.company}</div>
            <div><strong>Services:</strong> {buildResult.services_detected}</div>
            <div><strong>Dependencies:</strong> {buildResult.dependencies_detected}</div>
          </div>
        ) : (
          <div className="muted small">Build a graph to load platform data.</div>
        )}
      </div>
    </section>
  );
}