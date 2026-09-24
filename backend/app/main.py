from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.services.vector_store import vector_store
from app.api import search, image_search, change_detection, clustering


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize offline vector catalog on startup
    vector_store.load_or_create()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router)
app.include_router(image_search.router)
app.include_router(change_detection.router)
app.include_router(clustering.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "error_type": exc.__class__.__name__,
            "message": str(exc)
        }
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "indexed_tiles": len(vector_store.metadata)
    }
