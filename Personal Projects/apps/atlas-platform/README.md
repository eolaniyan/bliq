# Atlas Platform Intelligence

Atlas is an MVP platform intelligence system that:
- ingests synthetic enterprise architecture data
- builds a service dependency graph
- detects dependencies from configs, logs, and traces
- simulates blast radius for service failures
- generates simple runbook guidance

## Run locally

```bash
pip install -r requirements.txt
python synthetic_environment_generator/generate_company.py
uvicorn atlas_core.main:app --reload