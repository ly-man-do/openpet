# SPDX-License-Identifier: Apache-2.0
"""Fail if any STL part exceeds the printer build volume on any axis.

STL files are assumed to be exported in their documented print orientation,
so the axis-aligned bounding box is checked as-is. Reads ASCII and binary STL
with no third-party dependencies.

Usage: check_part_size.py [PATH ...]   (default: hardware/)
"""

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "hardware" / "core"))
from params import MAX_PART_SIZE, NEAR_LIMIT  # noqa: E402


def _ascii_vertices(data):
    for line in data.decode("ascii", errors="replace").splitlines():
        parts = line.split()
        if len(parts) == 4 and parts[0] == "vertex":
            yield tuple(float(v) for v in parts[1:])


def _binary_vertices(data):
    (count,) = struct.unpack_from("<I", data, 80)
    for i in range(count):
        offset = 84 + i * 50 + 12  # skip the normal
        coords = struct.unpack_from("<9f", data, offset)
        yield coords[0:3]
        yield coords[3:6]
        yield coords[6:9]


def stl_size(path):
    """Return the (x, y, z) bounding-box size of an STL file in mm."""
    data = Path(path).read_bytes()
    is_binary = len(data) >= 84 and 84 + struct.unpack_from("<I", data, 80)[0] * 50 == len(data)
    vertices = _binary_vertices(data) if is_binary else _ascii_vertices(data)
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    for v in vertices:
        for axis in range(3):
            lo[axis] = min(lo[axis], v[axis])
            hi[axis] = max(hi[axis], v[axis])
    if lo[0] == float("inf"):
        raise ValueError(f"{path}: no vertices found")
    return tuple(hi[axis] - lo[axis] for axis in range(3))


def find_stls(paths):
    for p in paths:
        p = Path(p)
        if p.is_file():
            yield p
        elif p.is_dir():
            yield from sorted(f for f in p.rglob("*") if f.suffix.lower() == ".stl")


def main(argv):
    paths = argv or [ROOT / "hardware"]
    failures = 0
    checked = 0
    for stl in find_stls(paths):
        checked += 1
        try:
            size = stl_size(stl)
        except (ValueError, struct.error) as err:
            print(f"ERROR {stl}: {err}")
            failures += 1
            continue
        dims = " x ".join(f"{s:.1f}" for s in size)
        if max(size) > MAX_PART_SIZE:
            print(f"FAIL  {stl}: {dims} mm exceeds {MAX_PART_SIZE:.0f} mm")
            failures += 1
        elif max(size[0], size[1]) > NEAR_LIMIT:
            print(f"NEAR  {stl}: {dims} mm (flag in BOM: full plate, no brim)")
        else:
            print(f"OK    {stl}: {dims} mm")
    print(f"{checked} part(s) checked, {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
