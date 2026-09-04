"""
Owned by "ML Engineer - Change Detection".
Pipeline, in order -- do not skip steps, this order is what makes the
false-alarm suppression actually work:
  1. register       -- align image B onto image A's geometry
  2. mask_invalid    -- flag cloud/shadow/haze pixels to exclude from comparison
  3. compute_diff    -- feature-level (not raw-pixel) difference
  4. classify_change -- label + confidence + earliest-observed date
"""
from typing import List, Dict


def register(image_a_path: str, image_b_path: str):
    """TODO: align image_b onto image_a (e.g. via rasterio reprojection or
    feature-based registration with OpenCV ORB/SIFT + homography)."""
    raise NotImplementedError


def mask_invalid(image_path: str):
    """TODO: return a boolean mask of cloud/shadow/haze-affected pixels to
    exclude from the diff. A simple starting point: brightness/NDSI thresholds;
    upgrade to a learned cloud classifier if time allows."""
    raise NotImplementedError


def compute_diff(image_a, image_b, mask_a, mask_b):
    """TODO: compare learned features (not raw pixel values) so seasonal
    color shifts don't register as change. Combine masks from both dates."""
    raise NotImplementedError


def classify_change(diff_map) -> Dict:
    """TODO: return {change_type, confidence, evidence_notes}."""
    raise NotImplementedError


def find_earliest_change(tile_stack: List[Dict]) -> Dict:
    """
    tile_stack: list of {date, image_path} sorted ascending by date for one AOI.
    Walk the stack pairwise, run the pipeline above, and return the first date
    where a change becomes visible and stays consistent across subsequent dates
    (this "confirmed across N observations" logic is what makes results trustworthy
    rather than a single noisy diff).
    """
    raise NotImplementedError
