#!/usr/bin/env python3
"""Statically validate the CS 498 Slurm templates and policy limits."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "--account": "26fa-cs498sw3-eng",
    "--partition": "eng-instruction",
    "--nodes": "1",
    "--ntasks": "1",
}
GPU_LIMITS = {
    "--cpus-per-task": "8",
    "--mem": "64G",
    "--gres": "gpu:A10:1",
}


def directives(path: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("#SBATCH "):
            continue
        token = line.removeprefix("#SBATCH ").strip()
        key, value = token.split("=", 1)
        found[key] = value
    return found


def require(path: Path, expected: dict[str, str]) -> None:
    found = directives(path)
    for key, value in expected.items():
        actual = found.get(key)
        if actual != value:
            raise AssertionError(f"{path.name}: expected {key}={value}, found {actual!r}")


def main() -> int:
    cpu = ROOT / "cs498_cpu.sbatch"
    gpu = ROOT / "cs498_gpu.sbatch"
    checkpoint = ROOT / "staff_gpu_checkpoint_test.sbatch"

    require(cpu, EXPECTED)
    for path in (gpu, checkpoint):
        require(path, EXPECTED | GPU_LIMITS)
        if directives(path).get("--time", "99:00:00") > "06:00:00":
            raise AssertionError(f"{path.name}: wall time exceeds six hours")

    for path in (ROOT / "README.md", ROOT / "POLICY.md"):
        text = path.read_text(encoding="utf-8")
        for required in ("26fa-cs498sw3-eng", "eng-instruction", "64 GB", "6 hours"):
            if required not in text:
                raise AssertionError(f"{path.name}: missing {required!r}")

    print("CS498_CLUSTER_TEMPLATE_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
