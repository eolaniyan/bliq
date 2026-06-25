import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from atlas_core import main


def write_repo(company_dir: Path, service: str, calls: list[str]) -> None:
    repos_dir = company_dir / "repos"
    repos_dir.mkdir(parents=True, exist_ok=True)
    (repos_dir / f"{service}.json").write_text(
        json.dumps({"service": service, "repo": f"{service}_repo", "calls": calls}),
        encoding="utf-8",
    )


class GraphCompanyScopeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.data_root = Path(self.tempdir.name)

        company_a = self.data_root / "company_a"
        company_b = self.data_root / "company_b"

        for company_dir in (company_a, company_b):
            (company_dir / "traces").mkdir(parents=True)
            (company_dir / "logs").mkdir(parents=True)
            (company_dir / "incidents").mkdir(parents=True)

        write_repo(company_a, "api_service", ["ledger_service"])
        write_repo(company_a, "ledger_service", [])

        write_repo(company_b, "checkout_service", ["inventory_service"])
        write_repo(company_b, "inventory_service", [])

        self.data_root_patch = patch.object(main, "DATA_ROOT", self.data_root)
        self.data_root_patch.start()
        self.client = TestClient(main.app)

    def tearDown(self) -> None:
        self.data_root_patch.stop()
        self.tempdir.cleanup()

    def test_company_scoped_reads_are_not_overwritten_by_later_build(self) -> None:
        response = self.client.post("/graph/build", params={"company": "company_a"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/graph/build", params={"company": "company_b"})
        self.assertEqual(response.status_code, 200)

        services = self.client.get("/graph/services", params={"company": "company_a"})
        self.assertEqual(services.status_code, 200)
        self.assertEqual(services.json()["services"], ["api_service", "ledger_service"])

        deps = self.client.get("/graph/dependencies/api_service", params={"company": "company_a"})
        self.assertEqual(deps.status_code, 200)
        self.assertEqual(deps.json()["dependencies"], ["ledger_service"])

        simulation = self.client.get("/graph/simulate/ledger_service", params={"company": "company_a"})
        self.assertEqual(simulation.status_code, 200)
        self.assertEqual(simulation.json()["direct_dependents"], ["api_service"])


if __name__ == "__main__":
    unittest.main()
