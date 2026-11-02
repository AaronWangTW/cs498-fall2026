"""Task 1: rasterize one LiDAR sweep into a four-channel BEV tensor.

Run directly with: python task1_bev.py
"""

import numpy as np

from hw3_utils import (
    DATA_ROOT, GRID_H, GRID_W, OUTPUT_ROOT, RESOLUTION, Z_MAX, Z_MIN,
    load_debug_frames, metric_to_grid, save_bev_boxes, save_bev_channels, write_json,
)


def rasterize_points(points: np.ndarray) -> np.ndarray:
    """Return `[4,400,352]` float32 BEV values in `[0,1]`.

    Input `points` has shape `[N,4]` with columns `(x,y,z,intensity)` in the
    LiDAR frame. The four output channels are max height, mean height, mean
    intensity, and log-density. Empty cells must be zero.

    Use `metric_to_grid`, a flat index `row * GRID_W + column`,
    `np.bincount` for counts/sums, and `np.maximum.at` for maximum height.
    Do not loop over BEV cells.
    """
    # ------------------------ Task 1 Modify your code below ---------------------
    res = np.zeros((4, GRID_H, GRID_W), dtype=np.float32)
    # following handout
    # filter points outside of ROI 
    # (doing this here cuz even though metric_to_grid does filtering as well, it doesn't do it for z)
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    intensity = points[:, 3]

    inROI = ((z >= Z_MIN) & (z <= Z_MAX)) # z filtering only to save time
    x = x[inROI]
    y = y[inROI]
    z = z[inROI]
    intensity = intensity[inROI]
    # flatten to flat index
    row, col, valid = metric_to_grid(x,y) 
    x = x[valid]
    y = y[valid]
    z = z[valid]
    intensity = intensity[valid]
    row = row[valid]
    col = col[valid]
    flat = row * GRID_W + col
    # counts per cell using bincount
    counts = np.bincount(flat,minlength=GRID_H * GRID_W)
    # sum per cell using bincount
    height_sum = np.bincount(flat,weights=z,minlength=GRID_H * GRID_W)
    intensity_sum = np.bincount(flat,weights=intensity,minlength=GRID_H * GRID_W)
    # max height per cell using np.maximum.at
    max_height = np.zeros(GRID_H * GRID_W, dtype=np.float32)
    np.maximum.at(max_height, flat, z)
    # mask of occupied cell for mean calculation
    occupancy = counts > 0
    # calculate mean height/intensity
    mean_height = np.zeros(GRID_H * GRID_W, dtype=np.float32)
    mean_intensity = np.zeros(GRID_H * GRID_W, dtype=np.float32)
    mean_height[occupancy] = height_sum[occupancy] / counts[occupancy]
    mean_intensity[occupancy] = intensity_sum[occupancy] / counts[occupancy]
    # normalize height
    max_height[occupancy] = (max_height[occupancy] - Z_MIN) / (Z_MAX - Z_MIN)
    mean_height[occupancy] = (mean_height[occupancy] - Z_MIN) / (Z_MAX - Z_MIN)
    # clip intensity instead of normalize as specified in handout
    mean_intensity = np.clip(mean_intensity, 0, 1)
    # density calculation
    density = np.log1p(counts) / np.log(65) # found log1p which is quite convenient for our operation
    density = np.clip(density, 0, 1) # clip instead of normalize again

    # fill in result
    res[0] = max_height.reshape(GRID_H, GRID_W)
    res[1] = mean_height.reshape(GRID_H, GRID_W)
    res[2] = mean_intensity.reshape(GRID_H, GRID_W)
    res[3] = density.reshape(GRID_H, GRID_W)

    return res
    # ---------------------- DO NOT MODIFY CODE OUTSIDE THE BLOCK ----------------


def main():
    points, boxes, frame_ids = load_debug_frames(DATA_ROOT / "debug_frames.npz")
    output = OUTPUT_ROOT / "task1"
    bev = rasterize_points(points[0])

    save_bev_channels(bev, output / "bev_channels.png")
    save_bev_boxes(bev, boxes[0], output / "bev_boxes.png", title=f"KITTI frame {frame_ids[0]}")

    occupied = np.max(bev, axis=0) > 0
    metrics = {
        "shape": list(bev.shape),
        "resolution_m": RESOLUTION,
        "occupied_cells": int(occupied.sum()),
        "occupancy_fraction": float(occupied.mean()),
        "channel_min": bev.reshape(4, -1).min(axis=1).tolist(),
        "channel_max": bev.reshape(4, -1).max(axis=1).tolist(),
    }
    write_json(output / "metrics.json", metrics)
    print("Checkpoint 1: bev_channels.png, bev_boxes.png, and metrics.json")
    return metrics


if __name__ == "__main__":
    print("Task 1 complete:", main())
