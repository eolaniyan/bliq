from threading import RLock

from atlas_core.graph.graph_builder import AtlasGraphStore


GRAPH_STORE = AtlasGraphStore()


class AtlasGraphRegistry:
    def __init__(self) -> None:
        self._stores: dict[str, AtlasGraphStore] = {}
        self._latest_company: str | None = None
        self._lock = RLock()

    def set_company_store(self, company: str, store: AtlasGraphStore) -> None:
        store.company_name = company
        with self._lock:
            self._stores[company] = store
            self._latest_company = company

    def get_store(self, company: str | None = None) -> AtlasGraphStore | None:
        with self._lock:
            if company is None:
                if self._latest_company is None:
                    return None
                return self._stores.get(self._latest_company)
            return self._stores.get(company)


GRAPH_REGISTRY = AtlasGraphRegistry()
