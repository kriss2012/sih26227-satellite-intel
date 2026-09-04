# Project Plan — SIH26227

Today: **Sept 3, 2026**. Deadline: **Sept 20, 2026** (17 days).
Assumes a 6-person team. If your team is smaller, merge roles marked with (*).

## Roles

| Role | Owns | Primary files |
|---|---|---|
| 1. Team Lead / Backend Owner | FastAPI app, integration, API contracts, deployment | `backend/app/main.py`, `core/`, `docker-compose.yml` |
| 2. ML Engineer — Retrieval | Text/image embeddings, FAISS/Qdrant index | `services/embedding_service.py`, `services/vector_store.py`, `api/search.py`, `api/image_search.py` |
| 3. ML Engineer — Change Detection | Registration, cloud/shadow masking, diffing, temporal logic | `services/change_detection_service.py`, `api/change_detection.py`, `api/clustering.py` |
| 4. Frontend Developer | Dashboard, map, time slider, before/after viewer | `frontend/src/**` |
| 5. Data/GIS Engineer (*) | Sourcing Sentinel-2/1 & Landsat tiles, tiling/COG prep, AOI selection | `docs/DATA_SOURCES.md`, ingestion scripts |
| 6. Docs/QA/PM (*) | Architecture note, provenance doc, evaluation report, testing, demo script | `docs/`, test suite |

If team is 4: merge (5) into (2)+(3), merge (6) into (1).

## Timeline

### Phase 1 — Setup & Data (Sept 3–5)
- **Sep 3**: Kickoff, assign roles, fork/clone this starter into your GitHub repo, everyone runs the quick-start locally. Pick one demo AOI (a real place with visible change, e.g. an area with recent construction) — the whole prototype should center on making that AOI's story compelling.
- **Sep 4**: Data engineer pulls Sentinel-2 tiles (and ideally Sentinel-1 SAR + one Landsat pass) for the AOI across 4–6 dates spanning a year+. Backend owner wires up config for local model/data paths.
- **Sep 5**: Finalize vector DB schema (embedding + lat/lon/date/sensor/cloud%) and API contracts. Everyone agrees on the JSON shapes in `models/schemas.py` — lock this early, it's what lets people work in parallel without blocking each other.

### Phase 2 — Core AI Pipeline (Sept 6–11)
- **Sep 6–7**: Preprocessing pipeline — read GeoTIFF/COG with rasterio, tile into fixed-size chips, normalize bands, basic cloud-mask flagging.
- **Sep 8–9**: Embedding model wired in (CLIP-style or a remote-sensing foundation model), tiles embedded and pushed into FAISS/Qdrant. Text query → embedding → nearest-neighbor search works end-to-end.
- **Sep 10–11**: Image-to-image search ("find similar locations") working off the same index. Sanity-check retrieval quality on the demo AOI.

### Phase 3 — Change Detection (Sept 12–15)
- **Sep 12–13**: Image registration/alignment between dates; build the false-alarm suppression layer (cloud/shadow/seasonal masking) before trusting any diff signal.
- **Sep 14**: Multi-temporal stack logic — walk the date-ordered image stack and estimate "earliest supported change" (this is a standout feature judges specifically look for).
- **Sep 15**: Clustering/"find similar sites" discovery feature, reusing the embedding index.

### Phase 4 — Frontend & Integration (Sept 16–18)
- **Sep 16**: Search bar + filters (date range, sensor, cloud%) + results grid, wired to real backend endpoints.
- **Sep 17**: Before/after viewer, change-map overlay (colored by change type), confidence score display, time slider across dates.
- **Sep 18**: Human-in-the-loop confirm/reject/needs-review buttons; full end-to-end integration pass with the real demo AOI data.

### Phase 5 — Harden, Document, Submit (Sept 19–20)
- **Sep 19**: **Offline validation** — physically disconnect the network and confirm the whole stack still runs (this constraint is graded, not optional). Fix bugs. Write the evaluation report (index size, build time, query latency, retrieval/change-detection accuracy on your demo AOI).
- **Sep 20**: Finalize architecture note, model/dataset provenance doc, incremental-ingestion writeup, record demo video, package submission.

## Daily team habit
15-minute standup each morning: what you shipped yesterday, what's blocking you, what you're doing today. Given the API contracts are locked on Sep 5, most blockers after that should be "I need the real model weights" or "I need sample data," not "I don't know what shape to return."

## Risk list (address these early, not on Sept 18)
- GDAL/rasterio install pain — resolve on Sep 3–4, not the night before demo.
- Foundation model weights are large — download and stage them locally well before the offline test on Sep 19.
- Real change-detection accuracy is hard — have a believable fallback (e.g. simpler thresholded diff + masking) if the fancier model underperforms; a working simple system beats a broken complex one.
