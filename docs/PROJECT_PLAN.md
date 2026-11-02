# OpenPet — Open-Source Companion Robot Pets

**Document:** Project Plan
**Document version:** 0.15.0 (draft)
**Date:** 2026-11-01
**Status:** Proposal — open decisions listed in Section 12
**Build order:** Dog first (Phases 0–11), then Cat (Phases 12–14)

> Versioning: this document has its own version (above). The project's hardware/software releases use separate semantic versions, starting at v0.1.0 when Phase 0 is complete (see Section 9).

---

## 1. Vision

OpenPet is a green-field, non-commercial, open-source project to build expressive companion robot pets from off-the-shelf electronics, existing open-source software, and 3D-printed parts.

There are two variants built on one shared platform:

| Variant | Inspiration | Personality |
|---|---|---|
| **OpenPet Dog** | Sony aibo ERS-1000 | Playful puppy: expressive body language, tricks, ball play, learns its owners |
| **OpenPet Cat** | Sox, the robot cat from *Lightyear* (fan build) | Loyal, talking companion: conversational, helpful, deadpan humour, expressive eyes |

Both variants share the same electronics, firmware, software stack and behaviour engine. Only the frame geometry, shell, gait parameters and personality profile differ.

## 2. Design Principles

1. **Shared core, swappable bodies.** Electronics, firmware, ROS 2 packages and "mind" are identical. Each pet is a configuration plus a body.
2. **Full expressiveness.** Every joint, sensor and behaviour that helps the character feel alive is in scope.
3. **Local first.** Everything runs on the robot. Cloud or desktop compute is an optional boost, never a requirement.
4. **Reuse before rebuild.** Adopt proven open-source projects for locomotion, perception, speech and simulation.
5. **FDM only.** Every printed part, structural and cosmetic, is made on a filament (FDM) printer: PETG/ASA/PLA+ for rigid parts, TPU for flexible parts. No resin printing.
6. **Versioned everything.** Hardware, firmware, software and docs are released together under one version number.
7. **Tracked in Beads.** All work (epics, issues, dependencies, status) lives in Beads inside the repo. This plan defines scope and exit criteria; Beads holds the live state of the work.

## 3. Variant Specifications

### 3.1 OpenPet Dog (aibo-inspired)

Matches the aibo ERS-1000 joint layout: 22 degrees of freedom.

| Body part | DOF |
|---|---|
| Head (pan, tilt, roll) | 3 |
| Mouth | 1 |
| Neck | 1 |
| Waist | 1 |
| Legs (hip abduction, hip, knee) × 4 | 12 |
| Ears × 2 | 2 |
| Tail (pan, tilt) | 2 |
| **Total** | **22** |

Senses: 2 animated eye displays, front camera, depth or ToF sensing, capacitive touch on head, chin and back, paw contact sensing, mic array, speaker, IMU, auto-docking charger.

### 3.2 OpenPet Cat (Sox-inspired)

Same core and joint vocabulary, re-proportioned for a cat body.

| Body part | DOF |
|---|---|
| Head (pan, tilt, roll) | 3 |
| Mouth (lip-sync while talking) | 1 |
| Neck | 1 |
| Waist / spine | 1 |
| Legs (hip abduction, hip, knee) × 4 | 12 |
| Ears × 2 | 2 |
| Tail (pan, tilt) | 2 |
| **Total** | **22** |

Character-specific features:

- **Full conversational speech** with a custom voice (local LLM + text-to-speech), mouth movement synced to speech
- Eye displays as the main channel for expression
- Cat behaviours: sitting upright, curling up, grooming gestures, slow blinks, head-bunting, kneading
- "Assistant" mode: reminders, timers, answering questions, reporting what it sees
- Room to add movie-inspired gadget props as cosmetic, non-functional accessories

> **Shell design note:** the cosmetic shell for the cat is a fan sculpt to be modelled by the project's builders from their own reference material. The plan keeps the shell as a separate module (Section 6.4) that bolts onto the shared frame, so the likeness can be refined without touching mechanics or electronics.

## 4. Existing Open-Source Building Blocks

| Project | What we reuse |
|---|---|
| **Petoi OpenCat** (MIT) | Skill/keyframe format, cat and dog gaits, behaviour patterns. Powers both Nybble (cat) and Bittle (dog), the closest existing precedent for a two-pet platform |
| **Stanford Pupper / Mini Pupper 2** | Inverse kinematics, trot controller, ROS 2 navigation and person tracking packages |
| **Stanford Pupper v3** | Reference for reinforcement-learning (RL) locomotion on a Raspberry Pi 5 and an animated display face |
| **MuJoCo Playground** (Apache-2.0) | GPU sim-to-real RL for walking, fall recovery and stand-up |
| **ROS 2 Lyrical Luth** | LTS middleware (supported to May 2031): nav2, slam_toolbox, tf, launch |
| **Raspberry Pi AI HAT+ 2** (Hailo-10H) | On-device vision plus local LLM/VLM, 40 TOPS, 8 GB on-board RAM |
| **Feetech SCS/STS SDK** | Serial-bus servo control with position, load and temperature feedback |
| Speech candidates | openWakeWord (wake word), whisper.cpp or Vosk (speech-to-text), Piper (text-to-speech engine; voice model loaded as a swappable asset) |
| Behaviour candidates | BehaviorTree.CPP or py_trees, plus a needs/emotion model |
| SLAM / vision candidates | slam_toolbox, RTAB-Map, YOLO on Hailo, face embeddings for recognition |

## 5. Shared System Architecture

```
                 +--------------------------------------------------+
                 |  Raspberry Pi 5 (16 GB) + AI HAT+ 2 (Hailo-10H)  |
                 |  Ubuntu 26.04 / ROS 2 Lyrical                    |
                 |                                                  |
  Cameras -----> |  Perception: faces, people, objects, SLAM, dock  |
  Mic array ---> |  Audio: wake word, STT, sound direction          |
                 |  Mind: personality profile + emotion model +     |
                 |        behaviour tree + long-term memory         |
                 |  Voice: LLM dialogue + TTS + lip-sync (cat)      |
                 |  Motion: RL policy / gait planner / skill player |
                 +---------------------+----------------------------+
                                       |  USB/UART (micro-ROS)
                 +---------------------v----------------------------+
                 |  ESP32-S3 body controller                        |
                 |  - Feetech servo bus(es), 1 Mbps                  |
                 |  - IMU @ 500 Hz, touch, paw contacts, BMS         |
                 |  - Eye displays, status LEDs, safety watchdog     |
                 +----+------------+------------+-------------+-----+
                      |            |            |             |
                 12 leg servos  10 expressive  2 eye       sensors,
                 (STS-series)   servos         displays    power
```

Optional **offboard brain**: the same ROS 2 graph can run heavier models (larger LLM, better voice) on a desktop, Jetson or rented cloud GPU over the network, with automatic fallback to on-board models. Day-to-day running stays on the robot; cloud is never required for the pet to work.

## 6. Hardware

### 6.1 Actuators (both variants)

| Joint group | Qty | Candidate | Notes |
|---|---|---|---|
| Legs | 12 | Feetech STS3215 (12 V, ~30 kg·cm) or STS3250 class | Magnetic encoder, daisy-chained bus, load feedback doubles as paw-touch and "being held" detection |
| Neck, waist | 2 | STS3215 | Carries head and body twist loads |
| Head, mouth, ears, tail | 8 | Feetech micro serial-bus servos (SCS0009 class) | Light, same protocol |

Upgrade path: quasi-direct-drive brushless actuators (as in Pupper v3) for a future high-performance body. This is a separate leg module, not a redesign.

### 6.2 Electronics

| Item | Candidate | Approx. cost (USD) |
|---|---|---|
| Main computer | Raspberry Pi 5, 16 GB, plus active cooler and microSD | 320–375 |
| AI accelerator | Raspberry Pi AI HAT+ 2 | 200–225 |
| Body controller | ESP32-S3 + Feetech bus adapter(s) + bench servo programmer | 35–64 |
| Cameras | Pi Camera Module 3 Wide (nose); optional Luxonis OAK-D Lite depth camera (+269, not in total) | 35–48 |
| IMU | BNO085 | 22–25 |
| Eyes | 2× round displays (GC9A01 LCD; round AMOLED is ~80–140 for two) | 16–30 |
| Touch | MPR121 + conductive pads (head, chin, back, cheeks) | 12–16 |
| Audio | 4-mic array (ReSpeaker XVF3800) + 3 W full-range speaker + I²S amp | 60–84 |
| Distance | VL53L5CX multizone ToF (obstacle + cliff) | 20–30 |
| Power | 3S Li-ion pack + BMS + 5 V/5 A regulator for Pi; charger and pogo-pin contacts; kill switch, fuse, wiring | 75–145 |
| Servos | 14× STS3215 + 8× SCS0009 micro bus servos (STS3250 legs would add ~700–800) | 344–608 |
| Dock | Charging dock with ArUco/IR beacon | 25–35 |
| Filament, fasteners, bearings, heat-set inserts | PETG/ASA/PLA+, TPU | 130–200 |
| **Estimated per pet** | | **~1,300–1,900** |

Prices were checked on 2026-11-01; the line-by-line BOM with suppliers is `hardware/bom/dog.csv`. Memory shortages raised Raspberry Pi prices sharply during 2026 (the Pi 5 16 GB launched at $120 and is now $305), so check again before ordering in Phase 2.

### 6.3 Frame (shared)

- **Sizing rule:** the robot's overall size is set by its largest printed part, which must fit the Bambu Lab P1S build volume of **256 × 256 × 256 mm** (see 6.5). The torso/spine is expected to be the largest part, so the dog is sized around a one-piece torso up to 256 mm long. Its other dimensions follow from the leg and head proportions.
- Modular chassis: spine/battery bay, shoulder and hip modules, leg modules, neck module, tail module.
- Dog and cat use the **same modules** with different link lengths, defined parametrically in CAD (one variable table per variant).
- Leg modules are interchangeable left/right where possible to reduce unique parts.
- Heat-set inserts, bearings on the opposite side of each servo horn, cable channels through every joint.

### 6.4 Shell (per variant)

- Snap-fit or magnetic cosmetic panels over the frame; no load passes through the shell.
- Dog shell and cat shell are separate CAD packages.
- Paint-ready surfaces; fine details (eye bezels, ears, badges) designed for FDM with a 0.4 mm nozzle (0.2 mm nozzle optional for small parts).
- TPU paw pads with embedded contact sensors.

### 6.5 CAD and Printing

- **CAD:** **build123d** (Python code-CAD, built on the OpenCascade kernel) so AI can write and edit every part directly (see Section 10.2). STEP + STL exports per release; FreeCAD or the OCP CAD Viewer (VS Code) for visual review.
- **Process:** FDM only. No resin parts anywhere in the BOM.
- **Reference printer:** Bambu Lab P1S (enclosed; 0.4 mm nozzle standard, 0.2 mm optional).
- **Part size limit:** every single printed part must fit within the P1S build volume of **256 × 256 × 256 mm**. This is the only size constraint on the design.
- **Near-limit parts:** parts approaching 256 mm in X or Y need Bambu Studio set to use the full print area and no brim. Each such part is flagged in the BOM with its slicer settings.
- **Automated check:** a CI script reads every STL in `hardware/` and fails the build if any part's bounding box exceeds 256 mm on any axis in its documented print orientation.
- **Materials on the P1S:** PETG and PLA+ for structure; ASA for heat-exposed parts near the Pi and servos (the enclosure suits ASA); TPU 95A for paws and bumpers, fed from an external spool rather than the AMS.
- **FDM design rules:** print orientation noted on every part, minimal supports, 0.2 mm layer default, heat-set inserts for all threaded joints, 3+ walls on load-bearing parts, smooth cosmetic faces oriented up or vertical.

## 7. Software Stack (shared)

| Layer | Approach |
|---|---|
| Firmware | ESP-IDF + micro-ROS; 500 Hz servo/IMU loop; safety behaviours (go limp, sit) on comms loss, overheat or low battery |
| Robot models | URDF + MJCF generated from CAD for each variant |
| Locomotion | RL policies trained per variant in MuJoCo Playground (walk, trot, turn, stand up, sit, lie); IK + keyframe skill player for expressive poses |
| Motion blending | Expressive animations layered over locomotion (tail wag while walking, head tracking while sitting) |
| Perception | Face recognition, person tracking, object/toy detection, sound localisation, SLAM for room awareness, dock detection |
| Mind | Personality profile (dog vs. cat), needs/emotion model, behaviour tree, long-term memory (people, places, routines) |
| Voice | Dog: vocalisations and optional speech. Cat: full dialogue with local LLM, owner-supplied TTS voice model, mouth lip-sync, eye expressions tied to sentiment |
| Tools | Web dashboard: teleop, live camera, skill/animation editor, personality tuning, logs, OTA updates |

### Personality profiles

| Trait | Dog | Cat |
|---|---|---|
| Primary output | Body language, barks | Speech, eyes, posture |
| Energy | High, playful | Calm, measured |
| Social drive | Seeks attention | Attentive and helpful, on its own terms |
| Signature behaviours | Fetch, beg, roll over, zoomies | Conversation, upright sitting, slow blink, curl up, head-bunt |

## 8. Repository Layout

```
openpet/
  design/
    concept/         # character brief, concept art, ROM table, split map, maquette
  hardware/
    core/            # shared frame modules, electronics
    dog/             # dog link lengths, shell
    cat/             # cat link lengths, shell
    electronics/     # KiCad carrier board, wiring
    bom/             # BOM per variant (CSV)
  firmware/          # ESP32 body controller
  ros2_ws/src/
    openpet_description/   # URDF/MJCF per variant
    openpet_bringup/
    openpet_control/
    openpet_perception/
    openpet_mind/          # behaviour + personality profiles
    openpet_voice/
  sim/               # MuJoCo models, RL configs per variant
  tools/dashboard/
  cloud/             # Docker images, job launch scripts (Section 10.6)
  docs/
    ai-log/          # AI decision log (Section 10.5)
  .beads/            # Beads issue database (epics, issues, dependencies)
  AGENTS.md          # instructions for AI agents: use bd for all task tracking
  CHANGELOG.md
  LICENSE-HARDWARE   # CERN-OHL-P-2.0
  LICENSE-SOFTWARE   # Apache-2.0
  LICENSE-DOCS       # CC BY 4.0
  THIRD_PARTY_LICENSES.md
```

### 8.1 Licensing

The project is released under the most permissive licences that suit each kind of material. Anyone can use, modify, share and sell builds or derivatives, with no requirement to open-source their changes; attribution is the only condition.

| Material | Licence | Why |
|---|---|---|
| Hardware (CAD source, STEP/STL, KiCad, BOM) | **CERN-OHL-P-2.0** | Permissive open-hardware licence written for physical designs |
| Software and firmware (ROS 2 packages, ESP32 firmware, tools, training code, build123d scripts) | **Apache-2.0** | Permissive, includes a patent grant, matches MuJoCo Playground and most of ROS 2 |
| Documentation, concept art, photos, videos | **CC BY 4.0** | Free reuse for any purpose with credit |
| Trained models (RL policies, vision) | **Apache-2.0** | Same terms as the software that produces them |
| Cat voice model | Not part of the project release | Supplied by you separately; kept outside the repo and outside these licences |

Rules:
- Every source file carries an SPDX licence header (e.g. `SPDX-License-Identifier: Apache-2.0`); CI checks for it
- Third-party code and models keep their own licences and are listed in `THIRD_PARTY_LICENSES.md`. Only permissive or weak-copyleft dependencies (MIT, BSD, Apache, LGPL used as a library) are accepted, so the whole stack stays as open as the project itself
- No contributor licence agreement; when contributions open (Phase 11), they are accepted under the same licences (inbound = outbound)
- The licences cover the project's own work. They don't grant rights to the Sox character, which the cat's fan shell is based on

## 9. Phased Roadmap

Each phase produces a working, tested result that the next phase builds on. A phase is finished only when its exit criteria pass. Its outputs are then tagged as a project release and logged in `CHANGELOG.md`.

### 9.1 Phase map

```
 DOG                                                          CAT
 P0  Foundation
  └─ P1  Design concept + motion envelope
      └─ P2  Core electronics + servo bus
          └─ P3  Single-leg test rig
              └─ P4  Chassis + standing dog  ──(URDF/MJCF)──┐
                  └─ P5  Walking (classical)                │
                      └─ P6  Simulation + RL locomotion <───┘
                          └─ P7  Expressive head, body + eyes
                              └─ P8  Senses
                                  └─ P9  Mind + personality
                                      └─ P10 Shell, paws + dock
                                          └─ P11 Dog v1.0 release
                                               └─ P12 Cat concept + body + locomotion
                                                   └─ P13 Cat voice + personality
                                                       └─ P14 Cat release (v2.0)
```

The **design concept (P1)** feeds every later phase: its joint range-of-motion table drives the leg rig (P3) and chassis (P4); its proportions drive the simulation model (P6); its shell split map and clearance zones drive the final shell (P10).

### 9.2 Phase summary

| Phase | Name | Builds on | Release |
|---|---|---|---|
| 0 | Foundation | — | v0.1.0 |
| 1 | Design concept + motion envelope | P0 | v0.2.0 |
| 2 | Core electronics + servo bus | P1 | v0.3.0 |
| 3 | Single-leg test rig | P1, P2 | v0.4.0 |
| 4 | Chassis + standing dog | P3 | v0.5.0 |
| 5 | Walking (classical controller) | P4 | v0.6.0 |
| 6 | Simulation + RL locomotion | P4, P5 | v0.7.0 |
| 7 | Expressive head, body + eyes | P6 | v0.8.0 |
| 8 | Senses | P7 | v0.9.0 |
| 9 | Mind + personality | P8 | v0.10.0 |
| 10 | Shell, paws + dock | P1, P9 | v0.11.0 |
| 11 | Dog v1.0 release | P10 | **v1.0.0** |
| 12 | Cat concept + body + locomotion | P11 | v1.1.0 |
| 13 | Cat voice + personality | P12 | v1.2.0 |
| 14 | Cat release | P13 | **v2.0.0** |

### 9.3 Phase details

#### Phase 0 — Foundation → v0.1.0
**Goal:** Set up the project and the AI-assisted workflow (Section 10) before any design or hardware work.
- Create a public GitHub repo on your personal account with the Section 8 layout, licence files (Section 8.1), `THIRD_PARTY_LICENSES.md`, CHANGELOG, and a short README noting the project is solo for now and not yet accepting contributions (see Section 10.8)
- CI checks for SPDX licence headers on every source file
- Install Beads (`bd`), run `bd init`, add `AGENTS.md`, and seed the epic/issue structure from this plan (Section 10.7)
- Set up the code-CAD environment (Section 6.5) with a shared parameter file for servo dimensions and printer limits
- Dev environment on development hosts (Section 10.9): ROS 2 Lyrical on Ubuntu 26.04 (arm64 container on an Apple-silicon Mac, or native on a Linux PC), ESP-IDF + micro-ROS toolchain, CI that builds the ROS workspace and firmware. The Pi 5 is not needed until Phase 2
- CI part-size check (STL bounding box ≤ 256 × 256 × 256 mm)
- P1S print profiles (PETG, PLA+, ASA, TPU) committed to the repo
- AI decision log started (`docs/ai-log/`)

**Exit criteria:** Beads initialised with all 15 phase epics, their dependency chain, and full issue breakdowns for P0 and P1; `bd ready` shows only P0 work; repo builds in CI; a "hello" ROS 2 node runs on a development host (Ubuntu 26.04 + ROS 2 Lyrical); a parametric test part builds from code-CAD to STL in CI; the part-size check rejects a deliberately oversized test STL.

#### Phase 1 — Design concept + motion envelope → v0.2.0
**Goal:** Lock the dog's look, feel and proportions together with how every limb moves, so the mechanics are designed around the character rather than the shell being forced around the mechanics.
**Builds on:** P0 code-CAD and simulation tooling.

*Look and feel*
- Character brief: age (puppy vs. young dog), temperament, how it should feel to watch and touch
- Mood board and style exploration (AI-generated concept art), narrowed to one original aibo-inspired direction
- Silhouette and proportion studies: head-to-body ratio, leg length, stance height, tail and ear shapes
- Face and eye design: eye display size and placement, eye animation style
- Colour, material and finish (CMF): filament colours, surface finish, paint/no-paint, TPU areas

*Motion envelope*
- Signature pose list (see table below) with a reference sketch for each
- Range-of-motion (ROM) table: required angle range for every one of the 22 joints, derived from the poses
- Kinematic block-out: simple code-CAD bodies on a jointed skeleton, loaded into MuJoCo and animated through every signature pose
- Clearance check: shell volumes tested for collisions across each joint's full ROM; gaps and sliding overlaps designed at shoulders, hips, neck, waist and tail root
- Shell split map: where each panel separates, aligned with joint boundaries so no panel spans a moving joint; every panel ≤ 256 mm
- Size envelope: overall length, height and width, with the torso as the largest part
- Weight and torque budget at the concept proportions (≥ 2× margin on leg joints)

*Physical check*
- Print a low-detail full-scale maquette (PLA, coarse layers) with pinned joints to check proportions, reach and clearances by hand

**Initial ROM targets** (to be confirmed by the block-out):

| Joint | Target range | Driven by |
|---|---|---|
| Hip abduction (×4) | −30° to +30° | Side-step, lying on side, roll over, getting up |
| Hip pitch (×4) | −100° to +120° | Sit, lie down, stretch (front legs forward), scratch |
| Knee (×4) | 0° to 150° | Lie down with legs tucked, sit, getting up |
| Neck pitch | −30° to +60° | Looking up at owner, sniffing floor |
| Head pan | −90° to +90° | Tracking people and sounds |
| Head tilt | −45° to +45° | Nodding, looking down at toys |
| Head roll | −35° to +35° | The "curious head tilt" |
| Mouth | 0° to 35° | Bark, yawn, hold a toy |
| Waist yaw | −25° to +25° | Turning to look back, wiggle, curling up |
| Ears (×2) | 0° to 90° | Alert, relaxed, flattened |
| Tail pan | −60° to +60° | Wagging |
| Tail tilt | −30° to +80° | Happy (up), sad (down) |

**Signature poses:** stand, sit, lie down (sphinx), lie on side, play bow, give paw, beg, stretch, roll over, scratch ear with hind leg, curious head tilt, sleep curled, stand up from each lying position.

**Deliverables:** Concept Design Document (`design/concept/`), concept renders, ROM table, block-out CAD + MJCF, animation clips of every signature pose, shell split map, size envelope, weight/torque budget, maquette photos.

**Exit criteria:** every signature pose reached in the block-out without self-collision or shell collision; ROM table frozen and every target achievable by the chosen servos and linkages; every planned part ≤ 256 mm; torque budget passes; concept direction approved by you.

#### Phase 2 — Core electronics + servo bus → v0.3.0
**Builds on:** P1 torque and weight budget (confirms servo choice and power sizing).
- Pi 5 bring-up: Ubuntu 26.04, ROS 2 Lyrical and the AI HAT+ 2 runtime; the Phase 0 hello node runs on the Pi
- Bench build: Pi 5 + AI HAT+ 2, ESP32-S3, Feetech bus adapter, IMU, 3S pack + BMS, 5 V regulator
- Firmware: servo bus driver (read/write position, load, temperature, voltage), IMU at 500 Hz, micro-ROS bridge to the Pi
- Safety layer: watchdog (servos go limp if the Pi stops talking), over-temperature and low-battery cut-offs, physical kill switch
- Joint limits from the P1 ROM table written into firmware as hard stops
- Wiring diagram v1 and first KiCad carrier-board schematic

**Exit criteria:** Pi commands 3 servos via ROS 2 at ≥ 200 Hz with telemetry back; firmware refuses commands outside ROM limits; watchdog and kill switch tested; Pi runs 30 min under full load with no brown-out.

#### Phase 3 — Single-leg test rig → v0.4.0
**Builds on:** P1 leg proportions and ROM, P2 electronics and firmware.
- Design and print one leg module (hip abduction, hip, knee) to the concept proportions, plus a bench test stand
- Leg inverse kinematics package (`openpet_control`)
- Test foot trajectories and the full ROM; measure current/torque under simulated body load; iterate link lengths
- Calibration routine (zero offsets stored per servo)

**Exit criteria:** leg reaches its full P1 ROM with no binding; follows a step trajectory with < 3 mm foot error; 30 min continuous stepping under 1.5× expected load without overheating; leg design frozen as the reference for all four legs.

#### Phase 4 — Chassis + standing dog → v0.5.0
**Builds on:** P3 frozen leg module, P1 size envelope and split map.
- Chassis: spine, battery bay, shoulder and hip modules, electronics mount, cable routing through every joint
- Dummy masses where the head, neck and tail will go, so the weight matches the finished dog
- Four leg modules, full 12-servo bus, power distribution
- URDF **and** MJCF models generated from the code-CAD, with measured masses
- Pose library: stand, sit, lie down, stretch, all smoothly blended

**Exit criteria:** dog stands for 10 min and moves between all poses without falling; URDF in RViz matches the real robot; MJCF ready for Phase 6.

#### Phase 5 — Walking (classical controller) → v0.6.0
**Builds on:** P4 standing robot.
- Port Stanford Pupper / Mini Pupper trot gait and body-pose controller to OpenPet
- IMU-based body levelling
- Teleop: gamepad and a first web dashboard (drive, pose buttons, battery, servo temps)

**Exit criteria:** walks 10 m on flat floor; turns on the spot; walks on carpet and hard floor; recovers from a light push without falling.

#### Phase 6 — Simulation + RL locomotion → v0.7.0
**Builds on:** P4 MJCF model, P5 real-world gait data as a baseline.
- Cloud setup (moved from Phase 0): GPU provider account and storage; project Docker image (MuJoCo + JAX/CUDA) built with pinned versions; a test job run end to end: launch, run, save results to storage, shut down (Section 10.6)
- System identification: match servo response, friction and mass in simulation to the real robot
- Train walk, turn, stand-up and fall-recovery policies in MuJoCo Playground on rented cloud GPUs, constrained to the P1 ROM
- Deploy policies on the Pi (ONNX), with the classical controller kept as a fallback

**Exit criteria:** RL walk beats the Phase 5 gait in speed or stability; dog gets up by itself from lying on either side; one-click switch between RL and classical controllers.

#### Phase 7 — Expressive head, body + eyes → v0.8.0
**Builds on:** P6 locomotion (the real head/neck/tail replace the dummy masses; policies retrained if mass changes), P1 face and eye design.
- Neck, 3-DOF head, mouth, ears, 2-DOF tail, waist joint
- Two animated eye displays with an expression library (happy, sleepy, curious, sad, surprised, love)
- Skill/animation editor in the dashboard (keyframes, timing, easing, save/load)
- Motion blending: expressive layers on top of locomotion (wag while walking, look around while standing)

**Exit criteria:** all 22 DOF working across their full ROM; all P1 signature poses performed on the real robot; 20+ skills; expressions play during walking without loss of balance.

#### Phase 8 — Senses → v0.9.0
**Builds on:** P7 head (cameras, mics and touch pads live in the head and body).
- Camera: person detection and tracking, face recognition (enrol owners), ball/toy detection on the Hailo
- Touch: head, chin, back, cheeks; paw contact from servo load and TPU paw sensors
- ToF: obstacle and cliff detection
- Audio: wake word, offline command set (sit, come, paw, lie down, good boy, etc.), sound-source direction

**Exit criteria:** dog turns to a voice and looks at the speaker; recognises 3 enrolled people; responds to 15+ voice commands; never walks off a table edge in testing.

#### Phase 9 — Mind + personality → v0.10.0
**Builds on:** P8 senses (inputs) and P7 skills (outputs), P1 character brief (personality targets).
- Needs/emotion model (energy, curiosity, affection, play, boredom)
- Behaviour tree driving autonomous life: explore, seek owner, play with ball, nap, ask for attention
- Long-term memory: people, preferences, daily routines, learned tricks
- Dog vocalisations (sample bank + procedural variation); optional speech via local LLM + TTS
- Personality tuning panel in the dashboard

**Exit criteria:** runs autonomously for 1 hour with varied, believable behaviour that matches the P1 character brief; responds differently to known vs. unknown people.

#### Phase 10 — Shell, paws + dock → v0.11.0
**Builds on:** P1 concept, CMF and shell split map; P9 complete robot.
- Final FDM dog shell built from the P1 concept: snap-fit/magnetic panels, vented zones, finished surfaces
- TPU paw pads and bumpers
- Charging dock with pogo pins and a visual marker; auto-docking when battery is low
- Room mapping (slam_toolbox or RTAB-Map) so the dog knows where the dock and its favourite spots are

**Exit criteria:** shell matches the approved concept; no rubbing or collisions at any joint limit (verified on the real robot across all signature poses); temperatures stay in spec with the shell on; dog docks from anywhere in a mapped room 9/10 times.

#### Phase 11 — Dog v1.0 release → v1.0.0
**Builds on:** P10 finished dog.
- Freeze hardware and software; 20-hour endurance test
- Full build guide (print settings, assembly, wiring, calibration, troubleshooting)
- BOM with suppliers, STL/STEP pack, flashing tools, SD-card image
- Open the project to the community (Section 10.8): CONTRIBUTING guide, code of conduct, GitHub Discussions or Discord, issue templates for builders
- Recruit at least 2 outside builders; they complete a dog from the docs alone

**Exit criteria:** outside builds succeed; all known critical bugs closed; v1.0.0 tagged.

#### Phase 12 — Cat concept + body + locomotion → v1.1.0
**Builds on:** P11 shared core; repeats the P1 concept process for the cat.
- Cat design concept: character brief, proportions, signature poses (upright sit, curl up, stretch, groom, knead, slow blink), ROM table, block-out, clearance check, shell split map
- Cat link-length table in the shared code-CAD; re-proportioned chassis and legs
- Cat URDF/MJCF; retrain RL policies for cat proportions and gait on rented cloud GPUs

**Exit criteria:** cat concept approved; cat walks, sits, lies and stands up using the same software stack with only configuration changes.

#### Phase 13 — Cat voice + personality → v1.2.0
**Builds on:** P12 cat body, P9 mind framework.
- Conversational pipeline: wake word → streaming speech-to-text → local LLM → TTS
- Mouth lip-sync and eye expressions tied to speech and sentiment
- Cat personality profile and assistant mode (reminders, timers, questions, reporting what it sees)
- **Voice slot:** TTS engine loads the voice model from a configurable path outside the repo (e.g. `~/.openpet/voices/cat/`). You supply the voice model; the AI builds and tests the pipeline using a stock placeholder voice until then
- Voice model files excluded from Git (`.gitignore`) and from release images
- Optional offboard brain for larger models

**Exit criteria:** average response latency < 2 s on-board; holds a multi-turn conversation; personality clearly distinct from the dog.

#### Phase 14 — Cat release → v2.0.0
**Builds on:** P13.
- Cat FDM shell (fan sculpt), TPU paws, dock reuse from the dog
- Cat build guide, BOM and image; outside builder test

**Exit criteria:** cat build reproduced by an outside builder; v2.0.0 tagged with both pets supported.

## 10. AI-Assisted Workflow

All phases are carried out with AI doing the design, code, analysis and documentation work. You direct, approve, and do the physical work (printing, assembly, wiring, testing), with AI guiding each step.

### 10.1 Who does what

| Activity | AI | You |
|---|---|---|
| Concept art, mood boards, proportion studies | Generates options, iterates on feedback | Choose direction, approve |
| CAD | Writes parametric code-CAD; exports STEP/STL; runs part-size and collision checks | Review renders, print, report fit issues |
| Electronics | Selects parts, writes wiring diagrams and KiCad schematics, power calculations | Order parts, solder, wire, measure |
| Firmware and ROS 2 | Writes, tests in simulation, debugs from logs | Flash, run, send back logs/videos |
| Simulation and RL | Builds models, launches training on rented cloud GPUs, tunes rewards | Run deployments on the robot, observe |
| Testing | Writes test procedures and checklists; analyses results | Execute tests, record results |
| Documentation | Writes build guides, BOMs, changelogs | Proofread by building from them |

### 10.2 Tooling choices that suit AI

- **Code-CAD (build123d, Python):** AI can write, read and modify every part directly as text. Parameters such as link lengths, servo sizes and the 256 mm limit live in one file. Diff-able in Git, and the URDF/MJCF can be generated from the same source.
- **Everything as text:** KiCad files, URDF/MJCF, behaviour trees, skill keyframes (JSON/YAML), personality profiles, test results (CSV).
- **Simulation first:** every mechanical and software change is checked in MuJoCo before it's printed or flashed.

### 10.3 Working loop per task

1. **Pick:** AI runs `bd ready` and claims the highest-priority unblocked issue
2. **Brief:** goal and constraints come from the issue description and its phase epic
3. **Generate:** AI produces design/code plus a test or check
4. **Verify in software:** CI checks, simulation, collision and size checks
5. **Build:** you print, assemble or flash (tracked as a `needs-human` issue)
6. **Report:** photos, video, logs or measurements back to the AI, noted on the issue
7. **Close or split:** AI closes the issue with a reason and commit reference, or files follow-up issues linked with `discovered-from`
8. **Gate:** when every issue in a phase is closed and the exit-criteria gate passes, tag the release and update `CHANGELOG.md`

### 10.4 Human checkpoints

These steps get a human check before going ahead, regardless of how confident the AI is:
- Battery, BMS and charging circuit wiring, before first power-on
- First power-on of every new board (current-limited bench supply)
- First motion of every new joint (low torque limit, robot on a stand)
- Approving the design concept (P1, P12) and final shell (P10)

### 10.5 AI decision log

`docs/ai-log/` records every significant AI-generated decision: the brief, options considered, the choice made, the version it landed in, and the Beads issue ID it came from. Beads holds the step-by-step audit trail of the work; the decision log holds the reasoning behind the bigger choices; `CHANGELOG.md` summarises what each release contains.

### 10.6 Cloud compute

All GPU-heavy work runs on **rented cloud GPUs**, paid by the hour, only while a job is running. Nothing in the project needs a local GPU. The cloud setup happens at the start of Phase 6, the first phase that needs it; earlier simulation work (such as the P1 block-out and collision sweeps) runs on the development hosts (Section 10.9).

**What runs in the cloud**

| Phase | Workload | Suggested GPU class |
|---|---|---|
| P6 | RL training: walk, turn, stand-up, fall recovery; system-ID sweeps | RTX 4090 / L40S class |
| P7 | Retraining policies after real head/tail masses are added | RTX 4090 / L40S class |
| P8 | Fine-tuning vision models (owner faces, toys) before compiling for the Hailo | RTX 4090 class |
| P12 | Cat RL training | RTX 4090 / L40S class |
| P13 | Optional LLM fine-tune for personality | A100/H100 class only if fine-tuning a larger LLM |

MuJoCo Playground runs on JAX with NVIDIA CUDA, so rentals must be NVIDIA GPUs.

**Providers:** RunPod, Vast.ai, Lambda or Modal; your choice. Launch scripts are written so jobs can run on more than one provider.

**How jobs run**
- One project Docker image (`cloud/`) with MuJoCo, JAX/CUDA, training code and pinned versions, so every run is reproducible
- AI-written launch scripts: start instance → pull image and repo at a tagged commit → train → upload checkpoints, logs and videos to storage → **auto-shutdown**
- Frequent checkpointing so interrupted (cheaper) instances can resume
- Experiment tracking (e.g. Weights & Biases free tier or TensorBoard logs in storage), linked from the AI decision log
- Trained policies exported to ONNX and committed (or released) with the version tag they belong to

**Costs:** managed by you outside this plan.

### 10.7 Work tracking with Beads

[Beads](https://github.com/steveyegge/beads) (`bd`) is a git-backed, dependency-aware issue tracker built for AI agents. It replaces markdown task lists so the AI keeps a persistent memory of the work across sessions.

**Structure**

```
Dog v1.0 (epic)                          Cat v2.0 (epic)
 ├─ P0 Foundation (epic)                  ├─ P12 Cat concept + body + locomotion (epic)
 │   ├─ issues (one per deliverable)      ├─ P13 Cat voice + personality (epic)
 │   └─ P0 exit gate (issue)              └─ P14 Cat release (epic)
 ├─ P1 Design concept + motion (epic)
 │   ├─ issues ...
 │   └─ P1 exit gate  ──blocks──> P2 epic
 ├─ ...
 └─ P11 Dog v1.0 release (epic) ──blocks──> Cat v2.0
```

| Plan element | Beads element |
|---|---|
| Pet release (Dog v1.0, Cat v2.0) | Top-level epic |
| Phase (P0–P14) | Child epic of its pet release |
| Deliverable bullet in a phase | Issue (task/feature) under that phase epic |
| Exit criteria | One "exit gate" issue per phase, listing each criterion as a checklist; closing it unblocks the next phase |
| "Builds on" links between phases | `blocks` dependencies between gate issues and epics |
| Human checkpoints (Section 10.4) | Issues labelled `needs-human`; AI cannot close them |
| Work found along the way | New issue linked `discovered-from` the issue that found it |

**Labels**
- Phase: `p0` … `p14`
- Area: `design`, `cad`, `electronics`, `firmware`, `ros`, `sim`, `ml`, `cloud`, `docs`, `print`, `assembly`, `test`
- Flags: `needs-human` (physical work or approval), `safety` (battery, power-on, first motion)

**Priorities:** P0 critical (blocks the phase) to P4 nice-to-have.

**Rules for the AI** (written into `AGENTS.md`)
- Use `bd` for all task tracking; no TODO lists in markdown
- Start every session with `bd ready`; claim an issue before working on it
- Only work on issues from the currently unblocked phase
- Never close a `needs-human` or `safety` issue; ask you instead
- Close issues with a reason and the commit or file reference
- File any new work as an issue straight away, linked to where it was found
- Exit-gate issues close only when every criterion has evidence attached (test result, photo, video or log)

**Seeding**
- Phase 0: create both pet epics, all 15 phase epics with their dependency chain, and full issue breakdowns for P0 and P1
- At the start of each later phase: expand that phase epic into issues from this plan, refined by what earlier phases learned

**How you see progress:** `bd ready` (what's next), `bd list` (everything), `bd show <id>` (detail and history), `bd dep tree <id>` (what blocks what).

### 10.8 Solo development, community later

OpenPet is developed **solo** (you plus AI) until the dog is ready for outside builders.

| Stage | Phases | Setup |
|---|---|---|
| Solo | P0–P10 | Public repo on your personal account; Beads is the only task tracker; GitHub Issues and PRs closed to outside contributions; README states the project is in solo development |
| Community | P11 onward | CONTRIBUTING guide, code of conduct, GitHub Discussions or Discord, builder issue templates; optional move to a GitHub organisation; outside contributions accepted under Section 8.1 licences |

While solo:
- No time spent on contributor onboarding, review processes or community moderation
- Docs are still written as if for an outside builder, so they are ready when the community opens
- Beads stays the source of truth; when the community opens, external bug reports from GitHub are mirrored into Beads issues

### 10.9 Development hosts

Phases 0 and 1 need no robot hardware. Their work runs on ordinary computers; the Raspberry Pi 5 is first needed for the Phase 2 bench build.

| Host | Used for |
|---|---|
| Apple-silicon Mac (MacBook Pro M1 Pro) | Code-CAD, MuJoCo simulation, ROS 2 in an arm64 Ubuntu 26.04 container (same CPU architecture as the Pi 5), firmware builds |
| Linux PCs | Native Ubuntu 26.04 + ROS 2 Lyrical, RViz with a display, USB to an ESP32-S3 dev board |
| Rented cloud GPUs | RL training (Section 10.6) |

Software written on the development hosts must run unchanged on the Pi: ROS 2 packages are tested in the arm64 container, and nothing may depend on macOS-only or x86-only libraries. Setup steps: `docs/setup/dev-hosts.md`.

## 11. Engineering Risks

| Risk | Mitigation |
|---|---|
| Weight vs. servo torque | Weight budget per variant from Phase 1; 12 V servos; RL policies trained with real mass data |
| Battery life | 3S pack, idle low-power poses, auto-docking |
| Heat | Vented shell zones, Pi active cooler, servo temperature monitoring |
| Pi 5 + Hailo power draw | Dedicated regulator, brown-out testing |
| Talking-cat latency | Streamed STT → LLM → TTS pipeline; offboard brain option |
| Cloud jobs interrupted or GPUs unavailable | Frequent checkpoints; resumable jobs; scripts work across more than one provider |
| Safety (pinch points, Li-ion) | Firmware torque limits, finger-safe gaps, BMS, charging guidance |

## 12. Open Decisions

None at this time. New decisions are added here as they come up.

Decided:
- Cloud GPU setup: **start of Phase 6**, when RL training first needs it, instead of Phase 0 (v0.14.0 of this plan)
- Development hosts: **Mac and Linux PCs** for Phases 0–1; the **Pi 5 is first needed in Phase 2** (v0.13.0 of this plan)
- Build order: **Dog first**, then Cat (v0.3.0 of this plan)
- Printing: **FDM only, no resin** (v0.3.0 of this plan)
- Size: **largest single part must fit the Bambu Lab P1S build volume, 256 × 256 × 256 mm**; overall robot size derived from that (v0.4.0 of this plan)
- Reference printer: **Bambu Lab P1S** (v0.4.0 of this plan)
- Workflow: **AI-assisted for all phases**, with you directing, approving and doing physical work (v0.5.0 of this plan)
- Compute: **rented cloud GPUs** for all training; no local GPU (v0.6.0 of this plan)
- Work tracking: **Beads** for epics, issues and dependencies (v0.7.0 of this plan)
- CAD library: **build123d** (v0.9.0 of this plan)
- Licensing: **as open as possible**: CERN-OHL-P-2.0 (hardware), Apache-2.0 (software, models), CC BY 4.0 (docs) (v0.10.0 of this plan)
- Team: **solo** (you plus AI) through Phase 10; community opens at Phase 11 (v0.11.0 of this plan)
- Cat voice: **supplied by you** in Phase 13 as a drop-in voice model; not produced by AI and not distributed with the project (v0.12.0 of this plan)
- Cloud costs: **managed by you**, outside the plan; no spend caps or approval steps (v0.8.0 of this plan)
- Design approach: **dedicated design concept phase (P1)** that covers look and feel together with limb motion (v0.5.0 of this plan)

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| 0.15.0 | 2026-11-01 | Section 6.2 prices checked against current listings (BOM in `hardware/bom/dog.csv`). Per-pet estimate rose from ~1,050–1,550 to ~1,300–1,900, mainly because the Pi 5 16 GB ($120 → $305) and AI HAT+ 2 ($130 → $200) went up with 2026 memory prices. Added lines the BOM was missing (Pi cooler and microSD, bench servo programmer, kill switch and wiring, charger). |
| 0.14.0 | 2026-11-01 | Moved the cloud GPU setup (account, Docker image, end-to-end test job) from Phase 0 to the start of Phase 6, the first phase that trains on GPUs. Removed the P1 cloud workload; P1 sweeps run on the development hosts. |
| 0.13.0 | 2026-11-01 | Added Section 10.9 (development hosts): Phases 0–1 run on an Apple-silicon Mac and Linux PCs, with ROS 2 Lyrical in an arm64 Ubuntu 26.04 container on the Mac. Phase 0 exit criterion changed from "hello node runs on the Pi" to "runs on a development host"; Pi 5 bring-up moved to the start of the Phase 2 bench build. |
| 0.12.0 | 2026-11-01 | Cat voice set as **owner-supplied**: Phase 13 now builds a swappable voice slot (model loaded from a path outside the repo, stock placeholder voice for development, voice files excluded from Git and releases). Removed AI voice training from Phase 13 and the cloud workload table. Voice model listed outside the project licences. All open decisions resolved. |
| 0.11.0 | 2026-11-01 | Set development to **solo** (you plus AI) through Phase 10, opening to the community at Phase 11. Added Section 10.8 (solo vs. community stages). Phase 0 now creates a public repo on your personal account with a solo-development README; CONTRIBUTING moved to Phase 11. Phase 11 now opens the community and recruits outside builders. Resolved the solo/community open decision. |
| 0.10.0 | 2026-11-01 | Licensing set to the most permissive options: hardware moved from CERN-OHL-W-2.0 to **CERN-OHL-P-2.0**, docs moved from CC BY-SA 4.0 to **CC BY 4.0**, software stays **Apache-2.0**, trained models added under Apache-2.0. Added Section 8.1 (licence table, SPDX headers with CI check, third-party licence list, dependency licence rule, no CLA, character-rights note). Phase 0 updated; licence open decision resolved. |
| 0.9.0 | 2026-11-01 | CAD library set to **build123d**; added OCP CAD Viewer for visual review; resolved the CAD open decision. |
| 0.8.0 | 2026-11-01 | Removed cloud cost controls (spend cap, approval threshold, cost log, rough budget, provider prices, `cloud-spend` label, cost-overrun risk, open decision); cloud costs are managed by you outside the plan. Fixed BOM price-check reference to Phase 0. |
| 0.7.0 | 2026-11-01 | Added **Beads** for AI work tracking: new design principle 7, Section 10.7 (epic hierarchy, mapping from plan to epics/issues/exit gates, dependency chain, labels, priorities, AI rules for `AGENTS.md`, seeding approach). Working loop (10.3) now starts from `bd ready` and ends at phase exit gates. Decision log now references Beads issue IDs. Phase 0 now initialises Beads and seeds epics; added `.beads/` and `AGENTS.md` to repo layout. |
| 0.6.0 | 2026-11-01 | Compute set to **rented cloud GPUs**. Added Section 10.6 (cloud workloads by phase, GPU classes, providers with Oct 2026 prices, Docker-based reproducible jobs, auto-shutdown, checkpointing, spend cap, cost log, rough budget). Phase 0 now includes cloud setup and a test job; P6, P12 and P13 train in the cloud. Added `cloud/` to repo layout, cloud risks, and cloud option for the offboard brain. Resolved the compute open decision. |
| 0.5.0 | 2026-11-01 | Added **Phase 1: Design concept + motion envelope** (look and feel, proportions, CMF, signature poses, 22-joint range-of-motion table with initial targets, kinematic block-out in MuJoCo, shell clearance check, shell split map, maquette). Renumbered phases: dog now P0–P11 (v1.0.0), cat P12–P14 (v2.0.0); cat phase now repeats the concept process. Size envelope and torque budget moved from P0 to P1. Later phases now reference P1 outputs (ROM limits in firmware, leg rig, RL constraints, final shell). Added **Section 10: AI-Assisted Workflow** (roles, AI-friendly tooling, working loop, human safety checkpoints, AI decision log). Switched CAD to Python code-CAD (build123d/CadQuery). Added `design/concept/` and `docs/ai-log/` to repo layout. Renumbered Risks (11) and Open Decisions (12); updated open decisions. |
| 0.4.0 | 2026-11-01 | Size rule set: largest single printed part must fit the Bambu Lab P1S build volume (256 × 256 × 256 mm); overall dog size derived from a one-piece torso up to 256 mm. P1S made the reference printer, with material guidance (PETG/PLA+/ASA/TPU). Added near-limit slicer guidance, CI part-size check, and P1S print profiles. Phase 0 now includes the size envelope and part-size check in its exit criteria. Open decisions updated (size and printer resolved). |
| 0.3.0 | 2026-11-01 | Build order set: **Dog first**, Cat after Dog v1.0. Replaced roadmap with 14 dependent phases (P0–P13), each with goal, dependencies, deliverables, exit criteria and a project release version (Dog v1.0.0, Cat v2.0.0). Added phase dependency map. Removed all resin printing; FDM only, with FDM design rules added. Separated document version from project release versions. Updated open decisions. |
| 0.2.0 | 2026-11-01 | Renamed project to **OpenPet**. Added two variants on a shared core: Dog (aibo-inspired) and Cat (Sox-inspired fan build). Restored full 22-DOF joint set for both variants. Removed self-imposed limits (budget cap, reduced DOF, no-speech rule, trademark section). Added conversational voice, lip-sync and assistant mode for the cat, plus personality profiles. Moved to Pi 5 16 GB, 12 V leg servos, 3S battery, optional offboard brain and brushless upgrade path. Split hardware into shared frame + per-variant shell. Updated repo layout, roadmap (added second-variant phase) and open decisions. |
| 0.1.0 | 2026-11-01 | First draft: vision, aibo reference specs, open-source building blocks, architecture, hardware BOM estimate, software stack, repo layout, roadmap, risks, open decisions. |
