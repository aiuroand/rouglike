"""Docstring"""
from typing import List
from typing import Tuple
import cv2
import numpy as np
from utils import apply_gaussian_2d

FAST_CIRCLE_RADIUS = 3
FAST_ROW_OFFSETS = [-3, -3, -2, -1, 0, 1, 2, 3, 3, 3, 2, 1, 0, -1, -2, -3]
FAST_COL_OFFSETS = [0, 1, 2, 3, 3, 3, 2, 1, 0, -1, -2, -3, -3, -3, -2, -1]
FAST_FIRST_TEST_INDICES = [0, 4, 8, 12]
FAST_FIRST_TEST_THRESHOLD = 3
FAST_SECOND_TEST_THRESHOLD = 12


def create_pyramid(
    img: np.ndarray, n_pyr_layers: int, downscale_factor: float = 1.2
) -> List[np.ndarray]:
    """
    Creates multi-scale image pyramid.

    Parameters
    ----------
    img : np.ndarray
        Gray-scaled input image.
    n_pyr_layers : int
        Number of layers in the pyramid.
    downscale_factor: float
        Downscaling performed between successive pyramid layers.

    Returns
    -------
    pyr : List[np.ndarray]
        Pyramid of scaled images.
    """
    pyr = [img]
    for k in range(n_pyr_layers - 1):
        new_im = cv2.resize(pyr[k], dsize=(round(pyr[k].shape[1] / downscale_factor), round(pyr[k].shape[0] / downscale_factor)))
        pyr.append(new_im)
    return pyr


# not necessary to implement, see README
def get_first_test_mask(
    img_level: np.ndarray, threshold: int, border: int
) -> np.ndarray:
    """
    Returns the mask from the first FAST test (FAST_FIRST_TEST_INDICES).

    Parameters
    ----------
    img_level : np.ndarray
        Image at the given level of the image pyramid.
    threshold : int
        Intensity by which tested pixel should differ from the pixels on its Bresenham circle.
    border: int
        Number of rows/columns at the image border where no keypoints should be reported.

    Returns
    -------
    mask : np.ndarray
        Boolean mask with True values at pixels which pass the first FAST test.
    """
    img_level = img_level.astype(int)
    border = max(border, FAST_CIRCLE_RADIUS)
    mask = np.zeros((img_level.shape[0], img_level.shape[1]), dtype=bool)
    for i in range(0 + border, img_level.shape[0] - border):
        for j in range(0 + border, img_level.shape[1] - border):
            l = 0
            d = 0
            for k in FAST_FIRST_TEST_INDICES:
                if img_level[i][j] > img_level[i + FAST_ROW_OFFSETS[k]][j + FAST_COL_OFFSETS[k]] + threshold:
                    l+=1
                elif img_level[i][j] < img_level[i + FAST_ROW_OFFSETS[k]][j + FAST_COL_OFFSETS[k]] - threshold:
                    d+=1
            if (d >= FAST_FIRST_TEST_THRESHOLD or l >= FAST_FIRST_TEST_THRESHOLD):
                mask[i][j] = True
    return mask


# not necessary to implement, see README
def get_second_test_mask(
    img_level: np.ndarray,
    first_test_mask: np.ndarray,
    threshold: int,
) -> np.ndarray:
    """
    Returns the mask from the second FAST test (FAST_FIRST_TEST_INDICES).
    HINT: test only at those points which already passed the first test (first_test_mask).

    Parameters
    ----------
    img_level : np.ndarray
        Image at the given level of the image pyramid.
    first_test_mask: np.ndarray
        Boolean mask for the first test, which was created by get_first_test_mask().
    threshold : int
        Intensity by which tested pixel should differ from the pixels on its Bresenham circle.

    Returns
    -------
    mask : np.ndarray
        Boolean mask with True values at pixels which pass the second FAST test.
    """
    img_level = img_level.astype(int)
    for i in range(0, img_level.shape[0]):
        for j in range(0, img_level.shape[1]):
            if first_test_mask[i][j]:
                l = 0
                d = 0
                for k in range(16):
                    if img_level[i][j] > img_level[i + FAST_ROW_OFFSETS[k]][j + FAST_COL_OFFSETS[k]] + threshold:
                        l+=1
                    elif img_level[i][j] < img_level[i + FAST_ROW_OFFSETS[k]][j + FAST_COL_OFFSETS[k]] - threshold:
                        d+=1
                if (d < FAST_SECOND_TEST_THRESHOLD and l < FAST_SECOND_TEST_THRESHOLD):
                    first_test_mask[i][j] = False
    return first_test_mask


def calculate_kp_scores(
    img_level: np.ndarray,
    keypoints: List[Tuple[int, int]],
) -> List[int]:
    """
    Calculates FAST score for initial keypoints.

    Parameters
    ----------
    img_level : np.ndarray
        Image at the given level of the image pyramid.
    keypoints: List[Tuple[int, int]]
        Tentative keypoints detected by FAST algorithm.

    Returns
    -------
    scores : List[int]
        Scores for the tentative keypoints.
    """
    img_level = img_level.astype(int)
    scores = []
    for i, j in keypoints:
        minimums = []
        for k in range(16):
            rolled_col = np.roll(FAST_COL_OFFSETS, k)
            rolled_row = np.roll(FAST_ROW_OFFSETS, k)
            minimum = 10000000
            for r in range(9):
                tmp = abs(img_level[i][j] - img_level[i + rolled_row[r]][j + rolled_col[r]])
                if tmp < minimum:
                    minimum = tmp
            minimums.append(minimum)
        scores.append(max(minimums))
    scores = [int(x) for x in scores]
    return scores


def detect_keypoints(
    img_level: np.ndarray,
    threshold: int,
    border: int = 0,
) -> Tuple[List[Tuple[int, int]], List[int]]:
    """
    Creates the initial keypoints list.

    Scans the image at the given pyramid level and detects the unfiltered FAST keypoints,
    which are upscaled according to the current level index.

    Parameters
    ----------
    img_level : np.ndarray
        Image at the given level of the image pyramid.
    threshold : int
        Intensity by which tested pixel should differ from the pixels on its Bresenham circle.
    border: int
        Number of rows/columns at the image border where no keypoints should be reported.

    Returns
    -------
    keypoints : List[Tuple[int, int]]
        Initial FAST keypoints as tuples of (row_idx, col_idx).
    scores: List[int]
        Corresponding scores calculate with calculate_kp_scores().
    """
    border = max(border, FAST_CIRCLE_RADIUS)
    keypoints, scores = [], []
    first_mask = get_first_test_mask(img_level=img_level, threshold=threshold, border=border)
    second_mask = get_second_test_mask(img_level=img_level, first_test_mask=first_mask, threshold=threshold)
    for i in range(0, img_level.shape[0]):
        for j in range(0, img_level.shape[1]):
            if second_mask[i][j]:
                keypoints.append((i, j))
    scores = calculate_kp_scores(img_level=img_level, keypoints=keypoints)
    return keypoints, scores


def get_x_derivative(img: np.ndarray) -> np.ndarray:
    """
    Calculates x-derivative by applying separable Sobel filter.
    HINT: np.pad()

    Parameters
    ----------
    img : np.ndarray
        Gray-scaled input image.

    Returns
    -------
    result : np.ndarray
        X-derivative of the input image.
    """
    img = img.astype(int)
    result = np.zeros((img.shape), dtype=int)
    ker = np.matrix([1,2,1]).T@np.matrix([1,0,-1])
    for i in range(1, img.shape[0] - 1):
        for j in range(1, img.shape[1] - 1):
            s = 0
            for k1 in range(-1,2):
                for k2 in range(-1,2):
                    s += ker[1+k1,1+k2] * img[i+k1][j+k2]
            result[i][j] = int(s) * -1
    return result


def get_y_derivative(img: np.ndarray) -> np.ndarray:
    """
    Calculates y-derivative by applying separable Sobel filter.
    HINT: np.pad()

    Parameters
    ----------
    img : np.ndarray
        Gray-scaled input image.

    Returns
    -------
    result : np.ndarray
        Y-derivative of the input image.
    """
    img = img.astype(int)
    result = np.zeros((img.shape), dtype=int)
    ker = np.matrix([1,0,-1]).T@np.matrix([1,2,1])
    for i in range(1, img.shape[0] - 1):
        for j in range(1, img.shape[1] - 1):
            s = 0
            for k1 in range(-1,2):
                for k2 in range(-1,2):
                    s += ker[1+k1,1+k2] * img[i+k1][j+k2]
            result[i][j] = int(s) * -1
    return result


def get_harris_response(img: np.ndarray) -> np.ndarray:
    """
    Calculates the Harris response.

    Calculates ixx, ixy and iyy from x and y-derivatives with Gaussian
    windowing (utils.apply_gaussian_2d(data=..., sigma=1.0). Then, uses the
    computed matrices to calculate the determinant and trace of the second-
    moment matrix. From it, calculates the final Harris response.

    Parameters
    ----------
    img : np.ndarray
        Gray-scaled input image.

    Returns
    -------
    harris_response : np.ndarray
        Harris response of the input image.
    """
    dx, dy = get_x_derivative(img), get_y_derivative(img)
    dx, dy = dx.astype(float) / 255.0, dy.astype(float) / 255.0
    ixx = dx*dx
    ixy = dx*dy
    iyy = dy*dy
    ixx_G = apply_gaussian_2d(sigma=1.0, data=ixx)
    ixy_G = apply_gaussian_2d(sigma=1.0, data=ixy)
    iyy_G = apply_gaussian_2d(sigma=1.0, data=iyy)
    harris_response = ixx_G*iyy_G - ixy_G*ixy_G - 0.05 * ((ixx_G+iyy_G)**2)
    return harris_response


def filter_keypoints(
    img: np.ndarray, keypoints: List[Tuple[int, int]], n_max_level: int
) -> List[Tuple[int, int]]:
    """
    Filters keypoints by Harris response.

    Iterates the detected keypoints for the given level. Sorts those keypoints
    by their Harris response in the descending order. Then, takes only the
    n_max_level top keypoints.

     Parameters
    ----------
    img : np.ndarray
        Gray-scaled input image.
    keypoints : List[Tuple[int, int]]
        Initial FAST keypoints.
    n_max_level : int
        Maximal number of keypoints for a single pyramid level.

    Returns
    -------
    filtered_keypoints : List[Tuple[int, int]]
        Filtered FAST keypoints.
    """
    harris_response = get_harris_response(img)
    l = []
    for i, j in keypoints:
        l.append((i, j, harris_response[i][j]))
    l = sorted(l, reverse=True, key=lambda a: a[2])
    filtered_keypoints = [(x, y) for (x, y, z) in l]
    filtered_keypoints = filtered_keypoints[:n_max_level]
    return filtered_keypoints


def fast(
    img: np.ndarray,
    threshold: int = 20,
    n_pyr_levels: int = 8,
    downscale_factor: float = 1.2,
    n_max_features: int = 500,
    border: int = 0,
) -> List[List[Tuple[int, int]]]:
    """
    Applies the modified FAST detector.

    Parameters
    ----------
    img : np.ndarray
        Gray-scaled input image.
    threshold: int
        Absolute intensity threshold for FAST detector.
    n_pyr_levels : int
        Number of layers in the image pyramid.
    downscale_factor: float
        Downscaling performed between successive pyramid layers.
    n_max_features : int
        Total maximal number of keypoints.
    """
    pyr = create_pyramid(img, n_pyr_levels, downscale_factor)
    keypoints_pyr = []
    # Adapt Nmax for each level
    factor = 1.0 / downscale_factor
    n_max_level, n_sum_levels = [], 0
    n_per_level = n_max_features * (1 - factor) / (1 - factor**n_pyr_levels)
    for level in range(n_pyr_levels):
        n_max_level.append(int(n_per_level))
        n_sum_levels += n_max_level[-1]
        n_per_level *= factor
    n_max_level[-1] = max(n_max_features - n_sum_levels, 0)
    for level, img_level in enumerate(pyr):
        keypoints, scores = detect_keypoints(img_level, threshold, border=border)
        idxs = np.argsort(scores)[::-1]
        keypoints = np.asarray(keypoints)[idxs][: 2 * n_max_level[level]].tolist()
        keypoints = filter_keypoints(img_level, keypoints, n_max_level[level])
        upscale_factor = downscale_factor**level
        keypoints = [
            (int(x * upscale_factor), int(y * upscale_factor)) for (x, y) in keypoints
        ]
        keypoints_pyr.append(keypoints)
    return keypoints_pyr
