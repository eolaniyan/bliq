import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export async function getCompanies() {
  const res = await api.get("/companies");
  return res.data;
}

export async function buildGraph(company) {
  const res = await api.post(`/graph/build?company=${company}`);
  return res.data;
}

export async function getServices() {
  const res = await api.get("/graph/services");
  return res.data;
}

export async function getDependencies(serviceName) {
  const res = await api.get(`/graph/dependencies/${serviceName}`);
  return res.data;
}

export async function getDependents(serviceName) {
  const res = await api.get(`/graph/dependents/${serviceName}`);
  return res.data;
}

export async function simulateFailure(serviceName) {
  const res = await api.get(`/graph/simulate/${serviceName}`);
  return res.data;
}

export async function getRunbook(serviceName) {
  const res = await api.get(`/graph/runbook/${serviceName}`);
  return res.data;
}

export async function getDrift(company) {
  const res = await api.get(`/graph/drift?company=${company}`);
  return res.data;
}

export async function getIncidents(company) {
  const res = await api.get(`/incidents?company=${company}`);
  return res.data;
}

export async function getServiceIncidents(company, serviceName) {
  const res = await api.get(`/incidents/${serviceName}?company=${company}`);
  return res.data;
}