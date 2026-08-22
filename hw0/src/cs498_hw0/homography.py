"""Starter interfaces for planar projective geometry.

Keep these public signatures unchanged: the tests and command-line tools use
them as the contract between the assignment handout and student code.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def estimate_homography(
    source_xy: ArrayLike, destination_xy: ArrayLike
) -> NDArray[np.float64]:
    """Estimate a 3 x 3 homography with normalized DLT.

    Args:
        source_xy: N x 2 source-plane coordinates, with N >= 4.
        destination_xy: N x 2 destination-image coordinates in matching order.

    Returns:
        A homography ``H`` such that ``destination ~ H @ source``.
    """
    del source_xy, destination_xy
    raise NotImplementedError("HW0 Task 1: implement normalized homography DLT")


def warp_image(
    image: ArrayLike, homography: ArrayLike, output_shape: tuple[int, int]
) -> NDArray[np.float64]:
    """Inverse-warp an image into ``(height, width)`` with bilinear sampling."""
    del image, homography, output_shape
    raise NotImplementedError("HW0 Task 2: implement inverse image warping")


def alpha_blend(foreground_rgba: ArrayLike, background_rgb: ArrayLike) -> NDArray[np.float64]:
    """Composite a floating-point RGBA foreground over an RGB background."""
    del foreground_rgba, background_rgb
    raise NotImplementedError("HW0 Task 2: implement alpha compositing")
