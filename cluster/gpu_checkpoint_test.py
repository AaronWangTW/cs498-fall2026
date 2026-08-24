#!/usr/bin/env python3
"""Run a bounded CUDA training loop and verify checkpoint reload."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=300)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()

    if not 30 <= args.seconds <= 1500:
        raise ValueError("--seconds must be between 30 and 1500")

    import torch

    if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
        raise RuntimeError(f"Expected exactly one CUDA device; found {torch.cuda.device_count()}")

    device = torch.device("cuda:0")
    torch.manual_seed(498)
    model = torch.nn.Sequential(
        torch.nn.Linear(1024, 2048),
        torch.nn.ReLU(),
        torch.nn.Linear(2048, 256),
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    started = time.time()
    steps = 0
    last_loss = 0.0
    while time.time() - started < args.seconds:
        inputs = torch.randn((256, 1024), device=device)
        targets = torch.randn((256, 256), device=device)
        optimizer.zero_grad(set_to_none=True)
        loss = torch.nn.functional.mse_loss(model(inputs), targets)
        loss.backward()
        optimizer.step()
        last_loss = float(loss.item())
        steps += 1

    args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(), "steps": steps}, args.checkpoint)

    reloaded = torch.nn.Sequential(
        torch.nn.Linear(1024, 2048),
        torch.nn.ReLU(),
        torch.nn.Linear(2048, 256),
    ).to(device)
    payload = torch.load(args.checkpoint, map_location=device, weights_only=True)
    reloaded.load_state_dict(payload["model"])

    result = {
        "status": "PASS",
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "gpu_name": torch.cuda.get_device_name(0),
        "steps": steps,
        "last_loss": last_loss,
        "elapsed_seconds": round(time.time() - started, 3),
        "checkpoint": str(args.checkpoint),
        "checkpoint_bytes": args.checkpoint.stat().st_size,
    }
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("CS498_GPU_CHECKPOINT_TEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

