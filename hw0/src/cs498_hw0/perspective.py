"""Starter interfaces for camera projection."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def estimate_projection_matrix(
    points_xyz: ArrayLike, pixels_uv: ArrayLike
) -> NDArray[np.float64]:
    """Estimate a 3 x 4 projection matrix from N >= 6 2D--3D pairs."""
    del points_xyz, pixels_uv
    raise NotImplementedError("HW0 Task 3: implement camera-matrix DLT")


def project_points(points_xyz: ArrayLike, projection: ArrayLike) -> NDArray[np.float64]:
    """Project N x 3 world points to N x 2 image coordinates."""
    del points_xyz, projection
    raise NotImplementedError("HW0 Task 3: implement homogeneous projection")
