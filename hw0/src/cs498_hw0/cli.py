"""Command-line environment check for HW0."""

from __future__ import annotations

import argparse

import numpy as np

from cs498_hw0 import homography, perspective, stereo


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cs498-hw0")
    parser.add_argument("command", choices=("check",), help="check imports and starter interfaces")
    return parser


def _check() -> int:
    interfaces = {
        "estimate_homography": homography.estimate_homography,
        "warp_image": homography.warp_image,
        "estimate_projection_matrix": perspective.estimate_projection_matrix,
        "project_points": perspective.project_points,
        "scale_intrinsics": stereo.scale_intrinsics,
        "ssd_disparity": stereo.ssd_disparity,
    }
    missing = [name for name, value in interfaces.items() if not callable(value)]
    if missing:
        raise RuntimeError(f"missing starter interfaces: {', '.join(missing)}")
    print(f"HW0 environment OK (NumPy {np.__version__}; {len(interfaces)} interfaces)")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "check":
        return _check()
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
