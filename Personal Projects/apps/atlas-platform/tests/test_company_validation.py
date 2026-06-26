import tempfile
import unittest
from pathlib import Path

from fastapi import HTTPException

from atlas_core import main
from atlas_core.graph.graph_queries import GRAPH_STORE
from atlas_core.models import ServiceNode


class CompanyValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.data_root = Path(self._tmpdir.name) / "synthetic_companies"
        self.data_root.mkdir()
        (self.data_root / "valid_company").mkdir()

        self._original_data_root = main.DATA_ROOT
        main.DATA_ROOT = self.data_root

        GRAPH_STORE.clear()

    def tearDown(self) -> None:
        GRAPH_STORE.clear()
        main.DATA_ROOT = self._original_data_root
        self._tmpdir.cleanup()

    def test_resolve_company_dir_accepts_direct_company_directory(self) -> None:
        self.assertEqual(
            main._resolve_company_dir("valid_company"),
            self.data_root / "valid_company",
        )

    def test_resolve_company_dir_rejects_traversal(self) -> None:
        for company in ("..", "../valid_company", "valid_company/..", "valid_company\\.."):
            with self.subTest(company=company):
                with self.assertRaises(HTTPException) as ctx:
                    main._resolve_company_dir(company)

                self.assertEqual(ctx.exception.status_code, 404)

    def test_build_graph_with_invalid_company_preserves_existing_graph(self) -> None:
        GRAPH_STORE.company_name = "previous_company"
        GRAPH_STORE.add_service(ServiceNode(name="critical_service"))

        with self.assertRaises(HTTPException) as ctx:
            main.build_graph("..")

        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(GRAPH_STORE.company_name, "previous_company")
        self.assertEqual(GRAPH_STORE.get_services(), ["critical_service"])


if __name__ == "__main__":
    unittest.main()
