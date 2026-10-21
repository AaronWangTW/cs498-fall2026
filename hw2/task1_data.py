"""Task 1: inspect, augment, and evaluate point-cloud labels.

Run directly with: python task1_data.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from hw2_utils import PART_NAMES, load_split, plot_point_clouds, write_json


# Student guidance:
# Input: points is a NumPy array with shape (N, 3), one XYZ coordinate per row.
# Output: return a new NumPy array with the same shape (N, 3).
# Rough idea: sample one random rotation around the z axis, one small global
# scale, and small independent Gaussian jitter, then apply them to a copy.
def augment_points(points, rng):
    """Apply a random z rotation, scale change, and coordinate noise."""
    # ---------------- Task 1B: INSERT YOUR CODE BELOW ----------------
    res = points.copy()
    # random rotation
    angle = rng.uniform(0.0,2.0*np.pi) # equivalent of 0 to 360 degrees but in radian
    # standard rotation matrix around z-axis (easily found online)
    R = np.array([
        [np.cos(angle),-np.sin(angle),0],
        [np.sin(angle),np.cos(angle),0],
        [0,0,1]
    ])
    res = res @ R.T # different from what's commonly used cuz different points array layout, but this preserves the shape
    # small global scale
    scale = rng.uniform(0.95,1.05) # "small" scale, not sure of the exact best values to use, but these should be small enough?
    res = scale * res
    # small Gaussian jitter
    jitter = rng.normal(0.0,0.01,size=res.shape) # "small" jitter, again not sure if too small or too large
    res = res + jitter
    return res.astype(points.dtype, copy=False) # Discovered a type mismatch issue when implementing task2 (test passed but real run doesn't)
    # debugging seems to trace back here, so return with type casting to make sure it's right
    # ------------ DO NOT MODIFY CODE OUTSIDE THIS BLOCK --------------


# Student guidance:
# Inputs: prediction and target can be shape (B, N) or any matching shape of
# integer class IDs in [0, num_classes). Output is shape (num_classes,
# num_classes), where rows are ground truth and columns are predictions.
# Rough idea: flatten both arrays, then count each (target, prediction) pair.
def compute_confusion_matrix(prediction, target, num_classes):
    """Return a matrix with ground-truth rows and prediction columns."""
    # ---------------- Task 1C: INSERT YOUR CODE BELOW ----------------
    M = np.zeros((num_classes, num_classes), dtype=np.int64)
    # flatten both arrays
    t = target.flatten()
    p = prediction.flatten()
    # count each (target, prediction) pair
    for i in range(len(t)):
        M[t[i],p[i]]+=1
    return M
    # ------------ DO NOT MODIFY CODE OUTSIDE THIS BLOCK --------------


# Student guidance:
# Input: confusion has shape (C, C), with ground-truth classes on rows and
# predicted classes on columns. Output: a float array with shape (C,).
# Rough idea: for each class, intersection is the diagonal entry; union is
# ground-truth count + predicted count - intersection. Use np.nan for union 0.
def iou_from_confusion(confusion):
    """Return one IoU per class; use NaN when the union is zero."""
    # ---------------- Task 1C: INSERT YOUR CODE BELOW ----------------
    # union is ground-truth count + predicted count - intersection.
    # ground-truth count + predicted count = row + col counts 
    # intersection = diagonal
    col = np.sum(confusion,axis=0)
    row = np.sum(confusion,axis=1)
    diag = np.diagonal(confusion)
    union = col + row - diag
    # Use np.nan for union 0, so initialize first then fill in with conditional division (cleanest way I can think of)
    res = np.full(len(confusion), np.nan, dtype=np.float64)
    np.divide(diag, union, out=res, where=(union != 0))
    return res
    # ------------ DO NOT MODIFY CODE OUTSIDE THIS BLOCK --------------


def main():
    root = Path(__file__).resolve().parent
    output = root / "outputs/task1"
    output.mkdir(parents=True, exist_ok=True)
    train = load_split(root / "data/train.npz")

    # Checkpoint 1A: inspect one chair and the class balance.
    plot_point_clouds(
        [train["xyz"][0]],
        [train["labels"][0]],
        ["Ground-truth chair parts"],
        output / "ground_truth.png",
    )
    counts = np.bincount(train["labels"].reshape(-1), minlength=len(PART_NAMES))
    figure, axis = plt.subplots(figsize=(6.4, 3.2))
    axis.bar(PART_NAMES, counts / counts.sum())
    axis.set(ylabel="fraction of points", title="Training-set class frequency")
    figure.tight_layout()
    figure.savefig(output / "class_frequency.png", dpi=180)
    plt.close(figure)
    print("Checkpoint 1A: ground_truth.png and class_frequency.png")

    # Checkpoint 1B: compare the original and augmented point clouds.
    augmented = augment_points(train["xyz"][0], np.random.default_rng(498))
    plot_point_clouds(
        [train["xyz"][0], augmented],
        [train["labels"][0], train["labels"][0]],
        ["Original", "Augmented"],
        output / "augmentation.png",
    )
    print("Checkpoint 1B: augmentation.png")

    # Checkpoint 1C: a perfect prediction should have IoU 1 for present classes.
    confusion = compute_confusion_matrix(train["labels"], train["labels"], len(PART_NAMES))
    per_class_iou = iou_from_confusion(confusion)
    metrics = {
        "perfect_prediction_miou": float(np.nanmean(per_class_iou)),
        "perfect_prediction_iou": per_class_iou.tolist(),
    }
    np.savetxt(output / "confusion_matrix.txt", confusion, fmt="%d")
    write_json(output / "metrics.json", metrics)
    print("Checkpoint 1C: confusion_matrix.txt and metrics.json")
    return metrics


if __name__ == "__main__":
    print("Task 1 complete:", main())
