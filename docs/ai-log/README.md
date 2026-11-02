<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# AI Decision Log

Records the reasoning behind significant AI-generated decisions (plan Section 10.5). Beads holds the step-by-step trail of the work; this log holds the *why* behind the bigger choices; `CHANGELOG.md` summarises each release.

One file per decision: `NNNN-short-title.md`, numbered in order, never renumbered. A later decision that changes an earlier one gets a new file that links back and sets the old one's status to "Superseded by NNNN".

```markdown
# NNNN — Title

- **Date:** YYYY-MM-DD
- **Beads issue:** openpet-xxxx
- **Version:** v0.x.0 (release it lands in)
- **Status:** Accepted | Superseded by NNNN

## Brief
What had to be decided and the constraints.

## Options considered
- Option A — pros / cons
- Option B — pros / cons

## Decision
What was chosen and why.

## Consequences
What this commits us to; what to revisit and when.
```
