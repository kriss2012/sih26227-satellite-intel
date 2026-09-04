from fastapi import APIRouter
from app.models.schemas import ChangeDetectionRequest, ChangeEvidence
from app.services import change_detection_service as cds

router = APIRouter(prefix="/change-detection", tags=["change-detection"])


@router.post("", response_model=ChangeEvidence)
def detect_change(request: ChangeDetectionRequest):
    """
    Compare the same location across two dates and return classified,
    confidence-scored change evidence (with false-alarm suppression applied).
    """
    # TODO: resolve (lat, lon, date_from) and (lat, lon, date_to) -> tile paths
    image_a_path, image_b_path = None, None
    aligned = cds.register(image_a_path, image_b_path)
    mask_a = cds.mask_invalid(image_a_path)
    mask_b = cds.mask_invalid(image_b_path)
    diff_map = cds.compute_diff(image_a_path, aligned, mask_a, mask_b)
    result = cds.classify_change(diff_map)
    return ChangeEvidence(**result)
