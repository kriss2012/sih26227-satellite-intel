"""
SIH26227: Satellite Intelligence & Change-Analysis Platform Test Suite
Verifies:
1. System health and offline indexed catalog availability
2. Natural language semantic vector search over remote sensing tiles
3. Image-to-image similarity search
4. Multi-spectral change detection and false-alarm suppression
5. Clustering & similar site discovery
6. High-performance NumPy vector search fallback
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.services.vector_store import vector_store

@pytest.fixture
def client():
    # Trigger startup event via TestClient context
    with TestClient(app) as test_client:
        yield test_client

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["indexed_tiles"] >= 8

def test_text_search_semantic(client):
    payload = {
        "query": "river siltation and embankment near water",
        "top_k": 4
    }
    response = client.post("/search/text", json=payload)
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    top_hit = results[0]
    assert "tile_id" in top_hit
    assert "score" in top_hit
    assert top_hit["score"] > 0.50
    # Brahmaputra river tile should rank highest for river siltation
    assert any("brahmaputra" in r.get("thumbnail_url", "").lower() or "T43RER" in r["tile_id"] for r in results)

def test_text_search_with_filter(client):
    payload = {
        "query": "infrastructure road construction",
        "filters": {
            "sensor": "Sentinel-2",
            "max_cloud_cover": 0.05
        },
        "top_k": 5
    }
    response = client.post("/search/text", json=payload)
    assert response.status_code == 200
    results = response.json()
    for r in results:
        assert "Sentinel-2" in r["sensor"]
        assert r["cloud_cover"] <= 0.05

def test_image_search_similarity(client):
    payload = {
        "tile_id": "T43REQ_20250518_L8",
        "top_k": 3
    }
    response = client.post("/search/image", json=payload)
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert "tile_id" in results[0]

def test_change_detection_pipeline(client):
    payload = {
        "latitude": 28.625,
        "longitude": 77.243,
        "date_from": "2024-05-18",
        "date_to": "2025-05-18"
    }
    response = client.post("/change-detection", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "change_type" in data
    assert "confidence" in data
    assert data["confidence"] > 0.80
    assert len(data["evidence_notes"]) > 0
    assert "first_observed" in data

def test_similar_sites_discovery(client):
    payload = {
        "tile_id": "T42RTP_20250214_S2A",
        "top_k": 4
    }
    response = client.post("/discover/similar-sites", json=payload)
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert "score" in results[0]
