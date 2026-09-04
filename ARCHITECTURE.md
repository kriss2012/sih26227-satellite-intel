# Architecture & Tech Stack — SIH26227

## Why this stack

Everything below is chosen for one reason first: **it has to run fully offline**
after models/weights/data are staged. That rules out any hosted API (OpenAI, cloud
vision APIs) and pushes everything toward local, open-weight models and local
databases.

## Layers

```
Analyst
   │
   ▼
React Dashboard  (search bar, filters, map, before/after viewer, time slider)
   │  HTTP/JSON
   ▼
FastAPI Backend  (orchestrates the three AI subsystems below)
   │
   ├─► Semantic Search     : text/image → embedding → FAISS/Qdrant lookup
   ├─► Change Detection    : registration → masking → diff → classification
   └─► Clustering/Discovery: embedding similarity over a region
   │
   ▼
Local Satellite Archive (GeoTIFF / Cloud-Optimized GeoTIFF)
```

## Frontend — React + Vite + Tailwind + MapLibre GL
- **Vite**: fast dev server, minimal config, plays well with a hackathon timeline.
- **Tailwind**: lets a small team build a clean dashboard without a design system.
- **MapLibre GL** (not Google Maps): open-source, works offline with local tile
  sources — required given the network constraint.

## Backend — Python + FastAPI
- Python because the entire remote-sensing/ML ecosystem (rasterio, GDAL, PyTorch,
  scikit-learn) lives there — using anything else means reimplementing geospatial
  tooling that already exists.
- FastAPI over Flask/Django: async support, automatic OpenAPI docs (useful for
  judges/evaluators inspecting your API), and Pydantic validation matches well
  with the strict request/response contracts this project needs.

## AI / Computer Vision
- **Embeddings (semantic + image search)**: a CLIP-style multimodal model, ideally
  one fine-tuned or pretrained on remote-sensing imagery (e.g. remote-sensing CLIP
  variants) rather than generic web-image CLIP — satellite imagery looks nothing
  like Instagram photos, so a remote-sensing-aware model will retrieve far better.
- **Change detection**: don't do raw pixel subtraction. The pipeline should be:
  1. **Registration** — align image pairs so the same pixel = the same ground location.
  2. **Quality masking** — flag/exclude cloud, shadow, and haze-affected regions.
  3. **Feature-level comparison** — compare learned features, not raw pixels, so
     seasonal color shifts (green→brown vegetation) don't register as "change."
  4. **Classification** — label the change type (construction, road, water, clearance).
- **Libraries**: PyTorch, OpenCV, rasterio, GDAL, GeoPandas, Shapely, scikit-learn.

## Vector search — FAISS (prototype) or Qdrant (fuller service)
- FAISS: simplest, fastest to stand up for an entirely local demo, no separate
  service to run.
- Qdrant: better if you want metadata filtering (date range, sensor, cloud%)
  combined with vector similarity in one query — more realistic for the "combine
  semantic + date + geography + sensor" filtering the problem statement asks for.
- Store alongside each embedding: `latitude, longitude, date, sensor, cloud_cover`.

## Data sources
See `docs/DATA_SOURCES.md`. Sentinel-2 (optical, best general-purpose), Sentinel-1
SAR (works through cloud cover), Landsat Collection 2 (long historical baseline),
Bhuvan/ISRO data (India-focused).

## The trap to avoid
A single "upload image → classifier says 'building'" tool does **not** satisfy
this problem statement. The judges are scoring an end-to-end discovery workflow:
query → search archive → retrieve candidates → compare across time → suppress
false alarms → rank by confidence → analyst confirms/rejects → provenance is
preserved. Build toward that full loop early, even if each stage is simple at
first — a thin end-to-end pipeline beats a deep but disconnected one.

## Standout features (add once the core loop works)
- Natural-language date-range queries ("water expansion between June 2025 and June 2026")
- Interactive change-map overlays with bounding polygons, not just a heatmap
- Time slider across all available dates for an AOI
- Explainable confidence scores ("93% — persistent structural change, low cloud
  contamination, confirmed across 3 observations")
- Human-in-the-loop confirm/reject that feeds back into future ranking
