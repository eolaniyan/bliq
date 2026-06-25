import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

function servicePath(serviceName) {
  return encodeURIComponent(serviceName);
}

export async function getCompanies() {
  const res = await api.get("/companies");
  return res.data;
}

export async function buildGraph(company) {
  const res = await api.post("/graph/build", null, { params: { company } });
  return res.data;
}

export async function getServices(company) {
  const res = await api.get("/graph/services", { params: { company } });
  return res.data;
}

export async function getDependencies(serviceName, company) {
  const res = await api.get(`/graph/dependencies/${servicePath(serviceName)}`, { params: { company } });
  return res.data;
}

export async function getDependents(serviceName, company) {
  const res = await api.get(`/graph/dependents/${servicePath(serviceName)}`, { params: { company } });
  return res.data;
}

export async function simulateFailure(serviceName, company) {
  const res = await api.get(`/graph/simulate/${servicePath(serviceName)}`, { params: { company } });
  return res.data;
}

export async function getRunbook(serviceName, company) {
  const res = await api.get(`/graph/runbook/${servicePath(serviceName)}`, { params: { company } });
  return res.data;
}

export async function getDrift(company) {
  const res = await api.get("/graph/drift", { params: { company } });
  return res.data;
}

export async function getIncidents(company) {
  const res = await api.get("/incidents", { params: { company } });
  return res.data;
}

export async function getServiceIncidents(company, serviceName) {
  const res = await api.get(`/incidents/${servicePath(serviceName)}`, { params: { company } });
  return res.data;
}
