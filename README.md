<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# OpenPet

Open-source companion robot pets built from off-the-shelf electronics, open-source software and FDM-printed parts.

- **OpenPet Dog**: a playful, aibo-inspired puppy with 22 degrees of freedom. Being built first.
- **OpenPet Cat**: a talking companion cat (fan build) on the same platform. Built after Dog v1.0.

Both pets share one set of electronics (Raspberry Pi 5 + AI HAT+ 2, ESP32-S3 body controller, Feetech serial-bus servos), firmware, ROS 2 software and behaviour engine. Only the frame proportions, shell, gait and personality differ.

> **Status: solo development.** OpenPet is being built by one person with AI assistance. Issues and pull requests are not open to outside contributions yet. The project opens to builders and contributors at Dog v1.0 (Phase 11).

## Where things are

| Path | Contents |
|---|---|
| [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md) | The project plan: scope, architecture, phases and exit criteria |
| `design/concept/` | Character brief, concept art, range-of-motion table, shell split map |
| `hardware/` | build123d code-CAD (shared core, dog, cat), electronics, BOMs, print profiles |
| `firmware/` | ESP32-S3 body controller (ESP-IDF + micro-ROS) |
| `ros2_ws/src/` | ROS 2 Lyrical packages |
| `sim/` | MuJoCo models and RL training configs |
| `cloud/` | Training Docker image and job scripts for rented GPUs |
| `docs/ai-log/` | Decision log |
| `.beads/` | Work tracking ([Beads](https://github.com/steveyegge/beads)); run `bd ready` to see what's next |

## Printing

Every part is printed on an FDM printer; the reference printer is the Bambu Lab P1S, and every part fits its 256 × 256 × 256 mm build volume. No resin.

## Licences

| Material | Licence |
|---|---|
| Hardware (CAD source, STEP/STL, KiCad, BOM) | [CERN-OHL-P-2.0](LICENSE-HARDWARE) |
| Software, firmware, trained models | [Apache-2.0](LICENSE-SOFTWARE) |
| Documentation, concept art, photos, videos | [CC BY 4.0](LICENSE-DOCS) |

Third-party components keep their own licences; see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

The cat is a non-commercial fan build. These licences cover OpenPet's own work only and grant no rights to the character it is inspired by. The cat's voice model is supplied separately by its owner and is not part of this project or its releases.
