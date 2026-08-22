import numpy as np
import pytest

from cs498_hw0 import homography, perspective, stereo


@pytest.mark.parametrize(
    ("function", "args", "kwargs"),
    [
        (homography.estimate_homography, (np.zeros((4, 2)), np.zeros((4, 2))), {}),
        (homography.warp_image, (np.zeros((2, 2)), np.eye(3), (2, 2)), {}),
        (homography.alpha_blend, (np.zeros((2, 2, 4)), np.zeros((2, 2, 3))), {}),
        (perspective.estimate_projection_matrix, (np.zeros((6, 3)), np.zeros((6, 2))), {}),
        (perspective.project_points, (np.zeros((1, 3)), np.zeros((3, 4))), {}),
        (stereo.scale_intrinsics, (np.eye(3), 2.0), {}),
        (
            stereo.ssd_disparity,
            (np.zeros((3, 3)), np.zeros((3, 3))),
            {"max_disparity": 2, "block_size": 3},
        ),
    ],
)
def test_starter_marks_student_work(function, args, kwargs):
    with pytest.raises(NotImplementedError):
        function(*args, **kwargs)
