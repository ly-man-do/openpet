<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# 0001 — Phase 0 foundation setup choices

- **Date:** 2026-11-01
- **Beads issue:** see the P0 "Repo skeleton" issue (`bd list --label p0`)
- **Version:** v0.1.0
- **Status:** Accepted

## Brief
Set up the repository, checks and tracking so that later phases can be built by AI with the owner approving and doing the physical work. Constraints: plan v0.12.0 (FDM only, 256 mm part limit, build123d, permissive licences, Beads, solo development).

## Options considered
- **Part-size check:** a mesh library (numpy-stl, trimesh) vs. a small dependency-free STL reader. The reader is ~40 lines, handles ASCII and binary STL, and keeps CI fast.
- **Oversized-part test:** commit an oversized STL fixture vs. generate it inside a test. A committed oversized part under `hardware/` would make the real check fail, so the tests generate fixtures in a temp directory.
- **SPDX check scope:** all files vs. source files only. Source files (code, build files, YAML/XML) are checked; Markdown docs carry a CC-BY-4.0 header comment by convention but are not enforced. Tool-generated Beads/agent files are excluded.
- **Printer and servo constants:** per-part constants vs. one shared `hardware/core/params.py`. Shared file, as the plan requires.

## Decision
As above. Servo dimensions in `params.py` come from datasheets and are marked to be verified with calipers before any servo-mating part is frozen. The cloud image installs unpinned packages until the first GPU build succeeds, then pins exact versions.

## Consequences
- Beads only lets an epic block another epic, so each phase epic is blocked by the previous phase *epic* rather than by its exit-gate task (plan Section 10.7 draws gate -> epic). The effect is the same: a phase epic closes only after its gate and all its issues are closed, and children of a blocked epic stay out of `bd ready`.
- STLs must be exported in print orientation, since the size check uses the axis-aligned bounding box as-is.
- The CI ROS job assumes a `ros:lyrical-ros-base` image and the firmware job ESP-IDF v5.5; both need confirming on the first GitHub run.
