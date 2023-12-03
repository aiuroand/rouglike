import math
import cv2
import pytest
import numpy as np
# from scipy.signal import convolve2d
# from scipy.spatial.distance import cdist
from pathlib import Path
# from utils import apply_gaussian_2d
import orb
import inspect
from pylint.lint import Run
from pylint.reporters import CollectingReporter

REF_PATH = Path(__file__).parent / "reference_out"
# Let student to solve detect_keypoints without helper mask arrays.
@pytest.mark.parametrize(
    "threshold,border", [[5, 0], [5, 10], [10, 0], [10, 20], [20, 0], [20, 20]]
)
def test_get_first_test_mask(input_image, threshold, border):
    img_base, img = input_image
    border = max(border, orb.FAST_CIRCLE_RADIUS)
    mask = orb.get_first_test_mask(img.astype(int), threshold, border)
    assert isinstance(mask, np.ndarray)
    assert mask.shape == img.shape
    assert mask[:border, :].sum() == 0
    assert mask[:, :border].sum() == 0
    assert mask[-border:, :].sum() == 0
    assert mask[:, -border:].sum() == 0
    mask_ref = np.load(REF_PATH / f"{img_base}_{threshold}_{border}_get_first_test_mask.npz")['mask_ref']
    x, y = img.shape
    assert (
        np.equal(mask, mask_ref).sum() / x / y > 0.98
    )  # might depend on dtype whether it is passed as int or np.uint8

