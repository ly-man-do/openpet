<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Changelog

All notable changes to OpenPet are recorded here. Hardware, firmware, software and docs share one version number; each phase that passes its exit gate is tagged as a release (see [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md), Section 9).

## [Unreleased] — Phase 0: Foundation (targets v0.1.0)

### Added
- Repository layout, licence files (CERN-OHL-P-2.0, Apache-2.0, CC BY 4.0), README, third-party licence list
- Project plan v0.12.0 in `docs/PROJECT_PLAN.md`
- Beads issue tracking with both pet epics, all 15 phase epics and exit gates, and full P0/P1 issue breakdowns
- `AGENTS.md` with the OpenPet rules for AI agents
- build123d code-CAD environment: shared parameters (`hardware/core/params.py`) and a fit-test coupon
- CI: SPDX header check, code-CAD build, 256 mm part-size check, ROS 2 workspace build, ESP32-S3 firmware build
- `openpet_bringup` hello node, ESP-IDF firmware skeleton
- Cloud training image skeleton (MuJoCo + MJX + Playground on JAX/CUDA) with a GPU smoke test
- AI decision log (`docs/ai-log/`)
- Priced dog BOM (`hardware/bom/dog.csv`), checked 2026-11-01
- Development hosts: `tools/dev/ros2.sh` (ROS 2 Lyrical in an arm64 Ubuntu 26.04 container) and `docs/setup/dev-hosts.md`; MuJoCo added to the dev requirements

### Changed
- Project plan v0.13.0: Phases 0–1 run on development hosts; Pi 5 bring-up moved to Phase 2
- Project plan v0.14.0: cloud GPU setup moved from Phase 0 to the start of Phase 6 (the `cloud/` image skeleton stays in the repo)
- Project plan v0.15.0: Section 6.2 prices updated; per-pet estimate now ~1,300–1,900 USD
