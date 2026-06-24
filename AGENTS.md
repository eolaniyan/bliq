# bliq

## Cursor Cloud specific instructions

The active project lives at `Personal Projects/apps/atlas-platform/` (note the spaces in the
path — always quote it in shell commands). It is the **Atlas Platform Intelligence MVP**:

- **Backend** (`atlas_core/`): a FastAPI app that ingests synthetic enterprise architecture
  data, builds a service dependency graph (networkx, in-memory), simulates failure blast
  radius, and generates runbooks. Run with:
  `.venv/bin/uvicorn atlas_core.main:app --reload` (serves on `http://localhost:8000`).
- **Frontend** (`atlas_ui/`): a React 19 + Vite app. Standard scripts in `atlas_ui/package.json`:
  `npm run dev` (Vite dev server on `http://localhost:5173`), `npm run lint` (eslint),
  `npm run build`. The frontend hardcodes the backend URL to `http://localhost:8000`
  (`src/api.js`), so the backend must be running on port 8000 for the UI to load data.

### Non-obvious notes

- The update script creates the Python venv at `Personal Projects/apps/atlas-platform/.venv`
  and installs frontend deps. Always invoke Python tools via that venv (`.venv/bin/...`); there
  is no project-level activation step assumed.
- Synthetic company data is committed under `synthetic_companies/`, so the backend works
  immediately with no data-generation step. To (re)generate data you can run
  `.venv/bin/python synthetic_environment_generator/generate_company.py`, but it is not required.
- There are no automated Python tests in this repo; verify the backend via its HTTP endpoints
  (e.g. `POST /graph/build?company=<name>`, `GET /graph/simulate/<service>`).
- `.env.example` is empty; no environment variables are required to run locally. The backend
  reads `ATLAS_DATA_ROOT` (optional) which defaults to the bundled `synthetic_companies/`.
