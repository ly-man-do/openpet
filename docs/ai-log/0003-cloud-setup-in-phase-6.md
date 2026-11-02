<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# 0003 — Set up cloud GPUs at the start of Phase 6

- **Date:** 2026-11-01
- **Beads issue:** openpet-8ci.1.14, openpet-8ci.1.15, openpet-8ci.1.16 (moved under the P6 epic, openpet-8ci.7)
- **Version:** v0.1.0 (plan document v0.14.0)
- **Status:** Accepted (owner's choice)

## Brief
Phase 0 required a cloud GPU account, a built training image and an end-to-end test job. Nothing uses a GPU until RL training in Phase 6, but P0 blocks P1, so this setup was holding up the design concept.

## Options considered
- **Keep in P0.** Proves the training pipeline early, but delays P1 and means paying for a provider account months before it's used.
- **Move to the start of P6.** P1 sweeps (block-out, collision checks) run on the Mac, where MuJoCo runs natively; the cloud is set up when training begins.

## Decision
Moved to the start of Phase 6. The `cloud/` Dockerfile and smoke test stay in the repo as a starting point.

## Consequences
- The training pipeline is first proven in P6, so P6 carries some setup risk; the existing smoke test keeps that step short.
- If a P1 sweep turns out too slow on the Mac, it can run on a Linux PC or the cloud setup can be pulled forward.
