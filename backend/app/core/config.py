"""
Central configuration for the backend.
Everything that points at a local file/model lives here so the rest of the
codebase never hardcodes a path — makes the "offline staging" requirement
easy to satisfy and easy to demo.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SIH26227 Satellite Intelligence API"

    # Local model weights — download once, point here, never fetch at runtime
    embedding_model_path: str = "./models/embedding_model"
    embedding_model_name: str = "ViT-B-32"  # open_clip model name, if used

    # Vector index
    vector_index_path: str = "./data/vector_index/faiss.index"
    vector_index_metadata_path: str = "./data/vector_index/metadata.jsonl"

    # Satellite archive
    archive_root: str = "./data/archive"  # COG/GeoTIFF tiles live here

    # Search
    default_top_k: int = 12

    class Config:
        env_file = ".env"


settings = Settings()
