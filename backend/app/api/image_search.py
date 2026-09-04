from fastapi import APIRouter, HTTPException
from app.models.schemas import ImageSearchRequest, SearchResult
from app.services import embedding_service
from app.services.vector_store import vector_store

router = APIRouter(prefix="/search", tags=["image-search"])


@router.post("/image", response_model=list[SearchResult])
def search_by_image(request: ImageSearchRequest):
    """
    'Find similar locations' -- given a tile the analyst already has, retrieve
    visually/semantically similar tiles from across the archive.
    """
    # TODO: resolve request.tile_id -> actual image path/array on disk
    tile_path = None
    if tile_path is None:
        raise HTTPException(status_code=501, detail="Wire tile_id -> archive path lookup")
    query_vector = embedding_service.embed_image(tile_path)
    filters = request.filters.model_dump() if request.filters else None
    results = vector_store.search(query_vector, top_k=request.top_k, filters=filters)
    return [SearchResult(**r) for r in results]
