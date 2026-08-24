#!/usr/bin/env python3
"""Verify a Slurm job has exactly one usable CUDA device."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        import torch
    except ImportError:
        print("PyTorch is not available. Load a supported module or activate the tested course environment.", file=sys.stderr)
        return 2

    if not torch.cuda.is_available():
        print("CUDA is not available inside this batch job.", file=sys.stderr)
        return 3

    device_count = torch.cuda.device_count()
    if device_count != 1:
        print(f"Expected exactly one visible GPU, found {device_count}.", file=sys.stderr)
        return 4

    started = time.time()
    device = torch.device("cuda:0")
    torch.manual_seed(498)
    left = torch.randn((2048, 2048), device=device)
    right = torch.randn((2048, 2048), device=device)
    product = left @ right
    torch.cuda.synchronize()

    result = {
        "status": "PASS",
        "hostname": platform.node(),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "torch_version": torch.__version__,
        "cuda_runtime": torch.version.cuda,
        "visible_gpu_count": device_count,
        "gpu_name": torch.cuda.get_device_name(0),
        "matrix_checksum": float(product[0, 0].item()),
        "elapsed_seconds": round(time.time() - started, 3),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("CS498_GPU_SMOKE_TEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

