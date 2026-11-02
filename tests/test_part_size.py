# SPDX-License-Identifier: Apache-2.0
import struct

import check_part_size


def write_binary_box(path, size):
    """Write a binary STL holding one triangle that spans the given box."""
    x, y, z = size
    triangle = struct.pack("<12fH", 0, 0, 1, 0, 0, 0, x, 0, 0, x, y, z, 0)
    path.write_bytes(b"\0" * 80 + struct.pack("<I", 1) + triangle)


def write_ascii_box(path, size):
    x, y, z = size
    path.write_text(
        "solid t\nfacet normal 0 0 1\nouter loop\n"
        f"vertex 0 0 0\nvertex {x} 0 0\nvertex {x} {y} {z}\n"
        "endloop\nendfacet\nendsolid t\n"
    )


def test_part_within_limit_passes(tmp_path):
    write_binary_box(tmp_path / "ok.stl", (200, 255.9, 30))
    assert check_part_size.main([str(tmp_path)]) == 0


def test_oversized_binary_part_rejected(tmp_path):
    write_binary_box(tmp_path / "too_big.stl", (100, 100, 256.5))
    assert check_part_size.main([str(tmp_path)]) == 1


def test_oversized_ascii_part_rejected(tmp_path):
    write_ascii_box(tmp_path / "too_big.stl", (300, 10, 10))
    assert check_part_size.main([str(tmp_path)]) == 1


def test_stl_size_reads_both_formats(tmp_path):
    write_binary_box(tmp_path / "b.stl", (10, 20, 30))
    write_ascii_box(tmp_path / "a.stl", (10, 20, 30))
    assert check_part_size.stl_size(tmp_path / "b.stl") == (10, 20, 30)
    assert check_part_size.stl_size(tmp_path / "a.stl") == (10, 20, 30)
