"""
Vector Store: FAISS index with high-performance pure NumPy fallback.
Supports incremental ingestion, filtering, and instant offline retrieval
without external network dependencies or difficult binary C-extensions.
"""
import json
import os
import hashlib
from typing import List, Dict, Optional
import numpy as np
from app.core.config import settings

try:
    import faiss  # type: ignore
except ImportError:
    faiss = None


DEFAULT_DEMO_TILES = [
    {
        "idx": 1,
        "tile_id": "T43RER_20250312_S2B",
        "latitude": 26.182,
        "longitude": 91.751,
        "date": "2025-03-12",
        "sensor": "Sentinel-2",
        "cloud_cover": 0.04,
        "description": "Brahmaputra river basin siltation, river embankment changes, and sandbar morphological shifts.",
        "thumbnail_url": "/tiles/brahmaputra_s2.jpg"
    },
    {
        "idx": 2,
        "tile_id": "T43REQ_20250518_L8",
        "latitude": 28.625,
        "longitude": 77.243,
        "date": "2025-05-18",
        "sensor": "Landsat",
        "cloud_cover": 0.08,
        "description": "Yamuna floodplain, rapid urban concrete expansion and linear road construction near river corridor.",
        "thumbnail_url": "/tiles/yamuna_l8.jpg"
    },
    {
        "idx": 3,
        "tile_id": "T42RTP_20250214_S2A",
        "latitude": 22.253,
        "longitude": 72.184,
        "date": "2025-02-14",
        "sensor": "Sentinel-2",
        "cloud_cover": 0.01,
        "description": "Dholera Special Investment Region mega-infrastructure grading, highway spur, and industrial park pads.",
        "thumbnail_url": "/tiles/dholera_s2.jpg"
    },
    {
        "idx": 4,
        "tile_id": "T42QVM_20250420_S2B",
        "latitude": 27.502,
        "longitude": 71.905,
        "date": "2025-04-20",
        "sensor": "Sentinel-2",
        "cloud_cover": 0.00,
        "description": "Thar Desert Bhadla solar park array expansion, high-reflectance photovoltaic fields and access tracks.",
        "thumbnail_url": "/tiles/bhadla_solar.jpg"
    },
    {
        "idx": 5,
        "tile_id": "T45QVG_20250130_S1A",
        "latitude": 21.942,
        "longitude": 88.891,
        "date": "2025-01-30",
        "sensor": "Sentinel-1",
        "cloud_cover": 0.00,
        "description": "Sundarbans mangrove tidal channels, storm surge shoreline retreat and surface water SAR backscatter.",
        "thumbnail_url": "/tiles/sundarbans_s1.jpg"
    },
    {
        "idx": 6,
        "tile_id": "T44VLM_20250610_S2A",
        "latitude": 34.204,
        "longitude": 78.106,
        "date": "2025-06-10",
        "sensor": "Sentinel-2",
        "cloud_cover": 0.05,
        "description": "Eastern Ladakh alpine valley, unpaved military road widening, bridge abutment construction, and river crossings.",
        "thumbnail_url": "/tiles/ladakh_s2.jpg"
    },
    {
        "idx": 7,
        "tile_id": "T43NKM_20250325_S2B",
        "latitude": 12.971,
        "longitude": 77.594,
        "date": "2025-03-25",
        "sensor": "Sentinel-2",
        "cloud_cover": 0.06,
        "description": "Bangalore peri-urban wetland transformation, encroached lake bed drying, and commercial building clusters.",
        "thumbnail_url": "/tiles/bangalore_s2.jpg"
    },
    {
        "idx": 8,
        "tile_id": "T43KBT_20250405_S2B",
        "latitude": 18.983,
        "longitude": 72.812,
        "date": "2025-04-05",
        "sensor": "Sentinel-2",
        "cloud_cover": 0.02,
        "description": "Mumbai Western Coast marine drive coastal reclamation, seawall barrier, and reclamation highway layout.",
        "thumbnail_url": "/tiles/mumbai_s2.jpg"
    }
]


class VectorStore:
    def __init__(self, dim: int = 512):
        self.dim = dim
        self.index = None
        self.metadata: List[Dict] = []
        # NumPy memory cache fallback
        self.numpy_vectors = np.empty((0, self.dim), dtype=np.float32)

    def load_or_create(self):
        """Loads FAISS index or initializes resilient NumPy fallback."""
        if faiss is not None and os.path.exists(settings.vector_index_path):
            try:
                self.index = faiss.read_index(settings.vector_index_path)
                with open(settings.vector_index_metadata_path, "r", encoding="utf-8") as f:
                    self.metadata = [json.loads(line) for line in f]
                return
            except Exception:
                pass

        if faiss is not None:
            base = faiss.IndexFlatIP(self.dim)
            self.index = faiss.IndexIDMap(base)
            self.metadata = []
        else:
            self.index = None
            self.metadata = []
            self.numpy_vectors = np.empty((0, self.dim), dtype=np.float32)

        # Seed initial high-quality demonstration catalog if empty
        self._seed_default_catalog()

    def _seed_default_catalog(self):
        from app.services.embedding_service import embed_text
        records = DEFAULT_DEMO_TILES
        vectors = []
        for r in records:
            v = embed_text(r["description"] + " " + r["sensor"])
            vectors.append(v)
        self.add(np.array(vectors, dtype=np.float32), records)

    def add(self, vectors: np.ndarray, records: List[Dict]):
        """Records must include a stable integer id under record['idx']."""
        vectors = vectors.astype(np.float32)
        # Normalize vectors for cosine similarity
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        vectors = vectors / norms

        if self.index is not None and faiss is not None:
            ids = np.array([r["idx"] for r in records], dtype=np.int64)
            self.index.add_with_ids(vectors, ids)
        else:
            self.numpy_vectors = np.vstack([self.numpy_vectors, vectors])

        self.metadata.extend(records)

    def search(self, query_vector: np.ndarray, top_k: int = 12,
               filters: Optional[Dict] = None) -> List[Dict]:
        """Performs cosine similarity search using FAISS or NumPy fallback."""
        q = query_vector.astype(np.float32).reshape(1, -1)
        q_norm = np.linalg.norm(q)
        if q_norm > 0:
            q = q / q_norm

        results = []
        if self.index is not None and faiss is not None:
            scores, ids = self.index.search(q, min(top_k * 4, max(1, len(self.metadata))))
            by_id = {r["idx"]: r for r in self.metadata}
            for score, idx in zip(scores[0], ids[0]):
                if idx == -1 or idx not in by_id:
                    continue
                record = by_id[idx]
                if filters and not self._passes_filters(record, filters):
                    continue
                # Normalize cosine score between 0.50 and 0.98
                norm_score = float(max(0.0, min(1.0, (score + 1.0) / 2.0)))
                results.append({**record, "score": round(norm_score, 4)})
                if len(results) >= top_k:
                    break
        else:
            if len(self.numpy_vectors) == 0:
                return []
            sims = np.dot(self.numpy_vectors, q.T).flatten()
            ranked_indices = np.argsort(-sims)
            for idx in ranked_indices:
                record = self.metadata[idx]
                if filters and not self._passes_filters(record, filters):
                    continue
                norm_score = float(max(0.0, min(1.0, (sims[idx] + 1.0) / 2.0)))
                results.append({**record, "score": round(norm_score, 4)})
                if len(results) >= top_k:
                    break

        return results

    @staticmethod
    def _passes_filters(record: Dict, filters: Dict) -> bool:
        if not filters:
            return True
        if filters.get("date_from") and record.get("date", "") < filters["date_from"]:
            return False
        if filters.get("date_to") and record.get("date", "") > filters["date_to"]:
            return False
        if filters.get("sensor") and filters["sensor"].lower() not in record.get("sensor", "").lower():
            return False
        if filters.get("max_cloud_cover") is not None and record.get("cloud_cover", 0.0) > filters["max_cloud_cover"]:
            return False
        if filters.get("bbox"):
            bbox = filters["bbox"]
            if len(bbox) == 4:
                min_lon, min_lat, max_lon, max_lat = bbox
                lat = record.get("latitude", 0.0)
                lon = record.get("longitude", 0.0)
                if not (min_lat <= lat <= max_lat and min_lon <= lon <= max_lon):
                    return False
        return True


vector_store = VectorStore()
