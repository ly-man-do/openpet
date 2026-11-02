<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# 0002 — Develop on a Mac and Linux PCs until the Pi 5 is needed

- **Date:** 2026-11-01
- **Beads issue:** openpet-8ci.1.18 (Pi bring-up moved to openpet-8ci.1.10 under P2)
- **Version:** v0.1.0 (plan document v0.13.0)
- **Status:** Accepted

## Brief
The owner has no Raspberry Pi 5 yet, but has a MacBook Pro (M1 Pro) and Linux-capable PCs. The P0 exit gate required a hello ROS 2 node on the Pi, and P0 blocks all of P1, so the missing Pi was holding up design work that never touches it.

## Options considered
- **Wait for the Pi.** Keeps the plan as written but stalls P1, which needs only CAD and simulation.
- **ROS 2 natively on macOS.** Not a supported tier for Lyrical, and it would drift from the Pi environment.
- **ROS 2 in an arm64 Ubuntu 26.04 container on the Mac, native Ubuntu on Linux PCs.** The Mac container has the same OS and CPU architecture as the Pi 5, so what runs there should run on the Pi unchanged.

## Decision
Use development hosts for Phases 0–1 (plan Section 10.9). The P0 criterion becomes "hello node runs on a development host". Pi 5 bring-up and its setup guide move to the start of the Phase 2 bench build, where the Pi is needed anyway. Verified on the Mac: `ros:lyrical-ros-base` is Ubuntu 26.04.1, aarch64; the hello node builds and runs via `tools/dev/ros2.sh`. MuJoCo 3.17.0 runs natively on the Mac and is now in `requirements-dev.txt`.

## Consequences
- Nothing in the software may depend on macOS-only or x86-only libraries.
- Phase 2 starts with Pi bring-up as a `needs-human`/`safety` issue (first power-on of a new board).
- An ESP32-S3 dev board would let firmware work start on the Mac or a Linux PC before the Pi arrives.
