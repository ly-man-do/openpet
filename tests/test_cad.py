# SPDX-License-Identifier: Apache-2.0
import pytest

build123d = pytest.importorskip("build123d")

import check_part_size  # noqa: E402
import params  # noqa: E402
import fit_coupon  # noqa: E402


def test_fit_coupon_builds_to_stl_within_build_volume(tmp_path):
    part = fit_coupon.build()
    assert part.volume > 0
    stl = tmp_path / "fit_coupon.stl"
    build123d.export_stl(part, str(stl))
    size = check_part_size.stl_size(stl)
    assert max(size) <= params.MAX_PART_SIZE
    assert check_part_size.main([str(stl)]) == 0
