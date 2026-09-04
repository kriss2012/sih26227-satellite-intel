"""
Thin wrapper around a FAISS index + a parallel metadata store.
Designed so new tiles can be added without rebuilding the whole index
(the "incremental ingestion" requirement in the problem statement).
"""
import json
import os
from typing import List, Dict, Optional
import numpy as np
from app.core.config import settings

try:
    import faiss  # type: ignore
except ImportError:
    faiss = None


class VectorStore:
    def __init__(self, dim: int = 512):
        self.dim = dim
        self.index = None
        self.metadata: List[Dict] = []

    def load_or_create(self):
        if faiss is None:
            raise RuntimeError("Install faiss-cpu (see requirements.txt)")
        if os.path.exists(settings.vector_index_path):
            self.index = faiss.read_index(settings.vector_index_path)
            with open(settings.vector_index_metadata_path) as f:
                self.metadata = [json.loads(line) for line in f]
        else:
            # IndexIDMap lets us add/remove by id -> supports incremental ingestion
            base = faiss.IndexFlatIP(self.dim)  # inner product on normalized vecs = cosine sim
            self.index = faiss.IndexIDMap(base)
            self.metadata = []

    def add(self, vectors: np.ndarray, records: List[Dict]):
        """records must include a stable integer id under record['idx']."""
        ids = np.array([r["idx"] for r in records], dtype=np.int64)
        self.index.add_with_ids(vectors.astype("float32"), ids)
        self.metadata.extend(records)
        self._persist()

    def search(self, query_vector: np.ndarray, top_k: int = 12,
                filters: Optional[Dict] = None) -> List[Dict]:
        scores, ids = self.index.search(query_vector.astype("float32").reshape(1, -1), top_k * 4)
        by_id = {r["idx"]: r for r in self.metadata}
        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx == -1 or idx not in by_id:
                continue
            record = by_id[idx]
            if filters and not self._passes_filters(record, filters):
                continue
            results.append({**record, "score": float(score)})
            if len(results) >= top_k:
                break
        return results

    @staticmethod
    def _passes_filters(record: Dict, filters: Dict) -> bool:
        # TODO: apply date_from/date_to, sensor, max_cloud_cover, bbox checks
        return True

    def _persist(self):
        os.makedirs(os.path.dirname(settings.vector_index_path), exist_ok=True)
        faiss.write_index(self.index, settings.vector_index_path)
        with open(settings.vector_index_metadata_path, "w") as f:
            for r in self.metadata:
                f.write(json.dumps(r) + "\n")


vector_store = VectorStore()
