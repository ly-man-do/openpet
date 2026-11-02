# SPDX-License-Identifier: Apache-2.0
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "ci"))
sys.path.insert(0, str(ROOT / "hardware" / "core"))
