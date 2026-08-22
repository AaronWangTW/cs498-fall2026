"""Starter interfaces for stereo geometry and matching."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def scale_intrinsics(intrinsics: ArrayLike, scale: float) -> NDArray[np.float64]:
    """Return intrinsics for an image resized by ``new_size = old_size / scale``."""
    del intrinsics, scale
    raise NotImplementedError("HW0 Task 5: implement intrinsic scaling")


def ssd_disparity(
    left: ArrayLike,
    right: ArrayLike,
    *,
    max_disparity: int,
    block_size: int,
) -> NDArray[np.float64]:
    """Compute left-image disparity with windowed sum of squared differences."""
    del left, right, max_disparity, block_size
    raise NotImplementedError("HW0 Task 6: implement SSD stereo matching")
