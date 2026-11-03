"""Task 2: encode metric 3D boxes as CenterPoint supervision targets.

Run directly with: python task2_targets.py
"""

import numpy as np

from hw3_utils import (
    DATA_ROOT, MAX_OBJECTS, NUM_CLASSES, OUT_H, OUT_W, OUTPUT_RESOLUTION,
    OUTPUT_ROOT, draw_gaussian, gaussian_radius, load_debug_frames,
    metric_to_output_grid, output_grid_to_metric, save_target_debug, write_json,
)
from task1_bev import rasterize_points


def encode_targets(boxes: np.ndarray) -> dict[str, np.ndarray]:
    """Encode `[M,7]` boxes into one dense heatmap and sparse regressions.

    Each box is `[x,y,z,length,width,height,yaw]`. Draw one Gaussian on the
    `[1,100,88]` center heatmap. At the integer center cell, store the flat
    index, sub-cell `(du,dv)`, center z, log-dimensions, and `(sin(yaw),
    cos(yaw))`. The mask marks valid rows among `MAX_OBJECTS` slots.
    """
    # ------------------------ Task 2A Modify your code below --------------------
    # initialization given by starter code
    res = {
        "heatmap": np.zeros((NUM_CLASSES, OUT_H, OUT_W), dtype=np.float32),
        "inds": np.zeros(MAX_OBJECTS, dtype=np.int64),
        "mask": np.zeros(MAX_OBJECTS, dtype=np.uint8),
        "reg": np.zeros((MAX_OBJECTS, 2), dtype=np.float32),
        "height": np.zeros((MAX_OBJECTS, 1), dtype=np.float32),
        "dims": np.zeros((MAX_OBJECTS, 3), dtype=np.float32),
        "rot": np.zeros((MAX_OBJECTS, 2), dtype=np.float32),
    }
    # converting coordinate system first to allow further processing
    x = boxes[:,0]
    y = boxes[:,1]
    u,v,valid = metric_to_output_grid(x,y)
    # filtering out the invalid ones for easier processing/result assignment
    boxes_valid = boxes[valid] 
    n = len(boxes_valid)
    res["mask"][:n] = 1 # marking the slots in use
    u = u[valid]
    v = v[valid]
    # calculate offsets for reg and normal coords
    cell_u = np.floor(u).astype(np.int64) # not casting would cause an error
    cell_v = np.floor(v).astype(np.int64)
    du = u - cell_u
    dv = v - cell_v
    res["reg"][:n] = np.column_stack((du,dv))
    # for inds
    flat = cell_v * OUT_W + cell_u
    res["inds"][:n] = flat
    # other values that can be assigned now that we have the valid boxes
    res["height"][:n,0] = boxes_valid[:,2] # z coord
    res["dims"][:n] = np.log(boxes_valid[:,3:6]) # log dimensions
    res["rot"][:n] = np.column_stack((np.sin(boxes_valid[:,6]),np.cos(boxes_valid[:,6]))) # sin(yaw),cos(yaw)
    # gaussian drawn by iterating through each box since we gotta use draw_gaussian and I don't wanna do the function map thing (laziness)
    # using helpers to draw/get radius
    for i in range(n):
        box = boxes_valid[i]
        # bev so height of box not needed, length -> x -> heat map width, 
        # width -> y -> heatmap height (x,y inversed for bev), unit need to be converted as well
        r = gaussian_radius(height=box[4] / OUTPUT_RESOLUTION,width=box[3] / OUTPUT_RESOLUTION) 
        # now actually just draw it
        draw_gaussian(res["heatmap"][0],center=(cell_u[i], cell_v[i]),radius=r)

    return res
    # ---------------------- DO NOT MODIFY CODE OUTSIDE THE BLOCK ----------------


def decode_targets(targets: dict[str, np.ndarray]) -> np.ndarray:
    """Invert `encode_targets` and return decoded metric boxes `[M,7]`."""
    # ------------------------ Task 2B Modify your code below --------------------
    # count first for easier initialization
    n = np.count_nonzero(targets["mask"])
    res = np.zeros((n, 7), dtype=np.float32)
    # retrieve x,y, need original u,v
    # first need cell_u,cell_v
    cell_u = targets["inds"][:n] % OUT_W
    cell_v = targets["inds"][:n] // OUT_W
    # then add du,dv, and use provided func
    du = targets["reg"][:n,0]
    dv = targets["reg"][:n,1]
    x,y = output_grid_to_metric(cell_u+du,cell_v+dv)
    res[:,0] = x
    res[:,1] = y
    # z is easy
    res[:,2] = targets["height"][:n,0]
    # dims just need exponent
    res[:,3:6] = np.exp(targets["dims"][:n,:])
    # yaw use atan2
    res[:,6] = np.atan2(targets["rot"][:n,0],targets["rot"][:n,1])

    return res
    # ---------------------- DO NOT MODIFY CODE OUTSIDE THE BLOCK ----------------


def main():
    points, boxes, frame_ids = load_debug_frames(DATA_ROOT / "debug_frames.npz")
    output = OUTPUT_ROOT / "task2"
    targets = encode_targets(boxes[0])
    decoded = decode_targets(targets)
    bev = rasterize_points(points[0])
    save_target_debug(targets["heatmap"], bev, boxes[0], decoded, output / "target_roundtrip.png")

    count = min(len(boxes[0]), len(decoded))
    center_error = (
        np.linalg.norm(boxes[0][:count, :2] - decoded[:count, :2], axis=1)
        if count else np.array([], dtype=np.float32)
    )
    metrics = {
        "frame_id": str(frame_ids[0]),
        "heatmap_shape": list(targets["heatmap"].shape),
        "heatmap_max": float(targets["heatmap"].max()),
        "ground_truth_boxes": int(len(boxes[0])),
        "encoded_boxes": int(targets["mask"].sum()),
        "decoded_boxes": int(len(decoded)),
        "mean_center_error_m": float(center_error.mean()) if len(center_error) else None,
    }
    write_json(output / "metrics.json", metrics)
    print("Checkpoint 2: target_roundtrip.png and metrics.json")
    return metrics


if __name__ == "__main__":
    print("Task 2 complete:", main())
