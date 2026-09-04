# SIH26227 — Offline Satellite Intelligence & Change-Analysis Platform

An offline-first platform where an analyst can search satellite imagery in natural
language, find visually similar locations, detect meaningful changes between dates,
and suppress false alarms caused by clouds, seasons, and lighting.

## Project structure

```
sih26227-satellite-intel/
├── README.md                  <- you are here
├── PROJECT_PLAN.md            <- team roles + day-by-day timeline to Sept 20
├── ARCHITECTURE.md            <- tech stack, data flow, design rationale
├── docs/
│   ├── DATA_SOURCES.md        <- Sentinel-2/1, Landsat, Bhuvan access notes
│   └── EVALUATION_CHECKLIST.md<- maps directly to what SIH judges will ask for
├── backend/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── app/
│       ├── main.py            <- FastAPI entrypoint
│       ├── core/config.py     <- settings (paths, model names, index paths)
│       ├── models/schemas.py  <- request/response Pydantic models
│       ├── api/
│       │   ├── search.py            <- POST /search/text
│       │   ├── image_search.py      <- POST /search/image
│       │   ├── change_detection.py  <- POST /change-detection
│       │   └── clustering.py        <- POST /discover/similar-sites
│       └── services/
│           ├── embedding_service.py       <- text/image embedding model
│           ├── vector_store.py            <- FAISS index wrapper
│           └── change_detection_service.py<- registration, masking, diffing
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── components/SearchBar.jsx
│       └── pages/Dashboard.jsx
├── docker-compose.yml
└── .gitignore
```

## Quick start (once dependencies are staged locally — see ARCHITECTURE.md)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Or with Docker: `docker-compose up --build`

## What's real here vs. what's a stub
Every backend module is a **working skeleton**: correct request/response contracts,
correct file layout, correct imports — but the actual model-loading and inference
logic has `# TODO` markers where your team plugs in the real embedding model, FAISS
index, and change-detection pipeline. This is intentional: it lets 3-4 people work
in parallel on separate files without merge conflicts from day one.
