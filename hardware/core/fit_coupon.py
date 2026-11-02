# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Parametric fit-test coupon: an STS3215 pocket with heat-set insert holes.

Print orientation: as modelled, base plate on the bed (Z up).
Prints in PETG, 0.2 mm layers, no supports. Used to tune the clearances in
params.py and to prove the code-CAD -> STL pipeline in CI.
"""

import argparse
import sys
from pathlib import Path

from build123d import Box, BuildPart, Cylinder, Locations, Mode, export_step, export_stl

sys.path.insert(0, str(Path(__file__).resolve().parent))
import params  # noqa: E402

WALL = 3.0
BASE = 3.0


def build():
    length, width, _ = params.STS3215.body
    pocket_l = length + 2 * params.CLEARANCE_SLIDING
    pocket_w = width + 2 * params.CLEARANCE_SLIDING
    pocket_depth = 10.0
    outer_l = pocket_l + 2 * WALL + 2 * 8.0  # room for an insert at each end
    outer_w = pocket_w + 2 * WALL
    height = BASE + pocket_depth

    with BuildPart() as coupon:
        Box(outer_l, outer_w, height)
        with Locations((0, 0, BASE / 2)):
            Box(pocket_l, pocket_w, pocket_depth, mode=Mode.SUBTRACT)
        insert = params.INSERT_M3
        x = pocket_l / 2 + WALL + 4.0
        with Locations((-x, 0, height / 2 - insert.depth / 2), (x, 0, height / 2 - insert.depth / 2)):
            Cylinder(insert.hole_diameter / 2, insert.depth, mode=Mode.SUBTRACT)
    return coupon.part


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("build/stl"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    part = build()
    export_stl(part, str(args.out / "fit_coupon.stl"))
    export_step(part, str(args.out / "fit_coupon.step"))
    bb = part.bounding_box()
    print(f"fit_coupon: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm -> {args.out}")


if __name__ == "__main__":
    main()
