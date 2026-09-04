"""
Owns text -> embedding and image -> embedding.
Whoever owns "ML Engineer - Retrieval" fills in the TODOs.
Keep this file's public function signatures stable -- api/search.py and
api/image_search.py depend on them.
"""
import numpy as np
from app.core.config import settings

_model = None
_preprocess = None
_tokenizer = None


def load_model():
    """
    TODO: load a CLIP-style model, ideally one pretrained/fine-tuned on
    remote-sensing imagery, from settings.embedding_model_path.
    Example (open_clip):
        import open_clip
        model, _, preprocess = open_clip.create_model_and_transforms(
            settings.embedding_model_name, pretrained=settings.embedding_model_path
        )
        tokenizer = open_clip.get_tokenizer(settings.embedding_model_name)
    Load once at startup (see app/main.py) and cache in module-level globals.
    """
    global _model, _preprocess, _tokenizer
    raise NotImplementedError("Load your embedding model here")


def embed_text(query: str) -> np.ndarray:
    """Return a normalized embedding vector for a natural-language query."""
    if _model is None:
        load_model()
    # TODO: tokenize `query`, run through the model's text encoder, L2-normalize
    raise NotImplementedError


def embed_image(image_path_or_array) -> np.ndarray:
    """Return a normalized embedding vector for one satellite tile."""
    if _model is None:
        load_model()
    # TODO: preprocess the tile (read with rasterio, resize/normalize bands),
    # run through the model's image encoder, L2-normalize
    raise NotImplementedError
