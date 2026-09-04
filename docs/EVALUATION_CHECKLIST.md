# Submission Checklist (maps to SIH26227's stated requirements)

- [ ] **Source code** — complete, reproducible, runs from a clean clone
- [ ] **Architecture note** — frontend, backend, AI models, database, vector
      index, geospatial processing, change detection (see `ARCHITECTURE.md`)
- [ ] **Index-building procedure** — documented steps: raw imagery → tiles →
      embeddings → vector index
- [ ] **Incremental ingestion** — show new tiles can be added to the index
      without a full rebuild (design this into `vector_store.py` from day one)
- [ ] **Model & dataset provenance** — for every pretrained model: name, source,
      version, license, weights location, purpose
- [ ] **Evaluation report** — indexed area, number of scenes/tiles, index build
      time, storage footprint, query latency, hardware used, retrieval quality,
      change-detection accuracy
- [ ] **Offline verification** — the whole system tested with network disabled
