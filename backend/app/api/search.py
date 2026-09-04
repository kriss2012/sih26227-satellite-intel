from fastapi import APIRouter
from app.models.schemas import TextSearchRequest, SearchResult
from app.services import embedding_service
from app.services.vector_store import vector_store

router = APIRouter(prefix="/search", tags=["semantic-search"])


@router.post("/text", response_model=list[SearchResult])
def search_by_text(request: TextSearchRequest):
    """
    Natural-language query -> embedding -> nearest neighbors in the vector index.
    e.g. "new structures near a river"
    """
    query_vector = embedding_service.embed_text(request.query)
    filters = request.filters.model_dump() if request.filters else None
    results = vector_store.search(query_vector, top_k=request.top_k, filters=filters)
    return [SearchResult(**r) for r in results]
