from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.services.vector_store import vector_store
from app.api import search, image_search, change_detection, clustering

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router)
app.include_router(image_search.router)
app.include_router(change_detection.router)
app.include_router(clustering.router)


@app.on_event("startup")
def startup():
    # Load the vector index once. Loading the embedding model here too (instead
    # of lazily) avoids a slow first request during the live demo.
    vector_store.load_or_create()


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}
