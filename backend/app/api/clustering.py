from fastapi import APIRouter
from app.models.schemas import SimilarSitesRequest, SearchResult
from app.services import embedding_service
from app.services.vector_store import vector_store

router = APIRouter(prefix="/discover", tags=["discovery"])


@router.post("/similar-sites", response_model=list[SearchResult])
def find_similar_sites(request: SimilarSitesRequest):
    """
    'Find Similar Sites' -- given one interesting location, cluster/rank other
    locations in the archive (optionally restricted to region_bbox) by similarity.
    """
    # TODO: resolve request.tile_id -> image path, embed it, then search restricted
    # to region_bbox via filters
    tile_path = None
    query_vector = embedding_service.embed_image(tile_path)
    filters = {"bbox": request.region_bbox} if request.region_bbox else None
    results = vector_store.search(query_vector, top_k=request.top_k, filters=filters)
    return [SearchResult(**r) for r in results]
