# SPDX-License-Identifier: Apache-2.0
import check_spdx


def test_header_accepted(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("# SPDX-License-Identifier: Apache-2.0\nprint(1)\n")
    assert check_spdx.check(f) is None


def test_missing_header_rejected(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("print(1)\n")
    assert check_spdx.check(f) is not None


def test_unknown_licence_rejected(tmp_path):
    f = tmp_path / "a.c"
    f.write_text("/* SPDX-License-Identifier: GPL-3.0-only */\n")
    assert check_spdx.check(f) is not None


def test_repo_is_clean():
    assert check_spdx.main([]) == 0
