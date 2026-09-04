"""
Request/response contracts shared by every API route.
Lock these on Day 3 (Sep 5) so frontend + backend can build in parallel.
"""
from typing import Optional, List
from pydantic import BaseModel


class Filters(BaseModel):
    date_from: Optional[str] = None       # ISO date, e.g. "2025-01-01"
    date_to: Optional[str] = None
    sensor: Optional[str] = None          # "Sentinel-2" | "Sentinel-1" | "Landsat"
    max_cloud_cover: Optional[float] = None
    bbox: Optional[List[float]] = None    # [min_lon, min_lat, max_lon, max_lat]


class TextSearchRequest(BaseModel):
    query: str
    filters: Optional[Filters] = None
    top_k: int = 12


class ImageSearchRequest(BaseModel):
    tile_id: str
    filters: Optional[Filters] = None
    top_k: int = 12


class ChangeDetectionRequest(BaseModel):
    latitude: float
    longitude: float
    date_from: str
    date_to: str


class SimilarSitesRequest(BaseModel):
    tile_id: str
    region_bbox: Optional[List[float]] = None
    top_k: int = 20


class SearchResult(BaseModel):
    tile_id: str
    latitude: float
    longitude: float
    date: str
    sensor: str
    cloud_cover: float
    score: float
    thumbnail_url: Optional[str] = None


class ChangeEvidence(BaseModel):
    change_type: str            # e.g. "construction", "road", "water", "clearance"
    confidence: float
    first_observed: Optional[str] = None
    evidence_notes: List[str] = []
    change_map_url: Optional[str] = None
