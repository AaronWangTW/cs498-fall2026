"""HW0 Task 3: two-view geometry and epipolar lines.

Work from Checkpoint 3A through 3C, then run:

    python task3_epipolar.py
"""

from pathlib import Path

import imageio.v3 as iio
import numpy as np

from hw0_utils import plot_two_views, symmetric_epipolar_distance, write_json


# ------------------------ Task 3: Modify your code below ------------------------

def estimate_fundamental_matrix(matches: np.ndarray) -> np.ndarray:
    """Estimate a rank-two F from rows (u1, v1, u2, v2), N >= 8.

    Replace the runnable placeholder with the normalized eight-point method:
    """
    # 1. normalize the points in each view independently;
    uv1 = matches[:,:2]
    cent1 = uv1.mean(axis=0)
    norm1 = uv1 - cent1
    dist1 = np.mean(np.sqrt(norm1[:,0]**2+norm1[:,1]**2))
    norm1 = norm1 / dist1

    uv2 = matches[:,2:]
    cent2 = uv2.mean(axis=0)
    norm2 = uv2 - cent2
    dist2 = np.mean(np.sqrt(norm2[:,0]**2+norm2[:,1]**2))
    norm2 = norm2 / dist2
    
    # 2. build the N x 9 design matrix from (u1, v1, u2, v2);
    N = len(matches)
    rows = []
    for i in range(N):
        u1 = norm1[i,0]
        v1 = norm1[i,1]
        u2 = norm2[i,0]
        v2 = norm2[i,1]
        r = np.array([u2*u1,u2*v1,u2,v2*u1,v2*v1,v2,u1,v1,1])
        rows.append(r)
    A = np.vstack(rows)
    # 3. solve its right null space with SVD;
    U,S,Vh = np.linalg.svd(A,full_matrices=True)
    rns = Vh[-1,:]
    # 4. enforce rank two by zeroing the smallest singular value; and
    F = rns.reshape((3,3))
    U,S,Vh = np.linalg.svd(F,full_matrices=True)
    Sig = np.diag([S[0],S[1],0])
    H = U @ Sig @ Vh
    # 5. denormalize and choose a stable scale.
    T_1 = np.array([[1/dist1,0,-cent1[0]/dist1],
                        [0,1/dist1,-cent1[1]/dist1],
                        [0,0,1]])
    T_2 = np.array([[1/dist2,0,-cent2[0]/dist2],
                        [0,1/dist2,-cent2[1]/dist2],
                        [0,0,1]])
    H = T_2.T@H@T_1
    H = H/np.mean(H)
        
    return H 


# ------------------- DO NOT MODIFY CODE OUTSIDE THE BLOCK --------------------


def main() -> dict[str, float | int]:
    """Run the three Task 3 checkpoints in the same order as the handout."""
    root = Path(__file__).resolve().parent
    output_dir = root / "outputs/task3"
    output_dir.mkdir(parents=True, exist_ok=True)
    all_matches = np.load(root / "data/epipolar/all_good_matches.npy")
    eight_matches = np.load(root / "data/epipolar/eight_good_matches.npy")
    images = [
        iio.imread(root / "data/epipolar/images/0000.png"),
        iio.imread(root / "data/epipolar/images/0005.png"),
    ]

    # Checkpoint 3A: estimate F from the supplied eight correspondences.
    fundamental = estimate_fundamental_matrix(eight_matches)
    np.savetxt(
        output_dir / "task3a_fundamental_matrix.txt",
        fundamental,
        fmt="%.10e",
        header="Estimated fundamental matrix F",
    )
    print(f"Checkpoint 3A saved; rank(F) = {np.linalg.matrix_rank(fundamental, tol=1e-8)}")

    # Checkpoint 3B: visualize matches first, then the epipolar lines from F.
    plot_two_views(images, all_matches, output_dir / "task3b_correspondences.png")
    plot_two_views(images, all_matches, output_dir / "task3b_epipolar_lines.png", fundamental)
    print("Checkpoint 3B saved: correspondences and epipolar lines")

    # Checkpoint 3C: evaluate F on all 200 correspondences.
    errors = symmetric_epipolar_distance(all_matches, fundamental)
    metrics: dict[str, float | int] = {
        "fundamental_rank": int(np.linalg.matrix_rank(fundamental, tol=1e-8)),
        "mean_symmetric_epipolar_error_px": float(np.mean(errors)),
        "median_symmetric_epipolar_error_px": float(np.median(errors)),
    }
    write_json(output_dir / "task3c_metrics.json", metrics)
    np.savez(output_dir / "task3_results.npz", fundamental=fundamental)
    print("Checkpoint 3C saved: task3c_metrics.json")
    return metrics


if __name__ == "__main__":
    print("Task 3 complete:", main())
