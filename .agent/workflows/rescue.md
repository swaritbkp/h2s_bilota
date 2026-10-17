---
description: Anytime emergency: revert to last green checkpoint, apply the cut line, protect the submission floor and the demo.
---

# Workflow: `/rescue`

Trigger when the build is broken, a phase overran by more than 25%, or less than 30% of time remains and the happy path is not demo-ready.

When triggered:
1. **Triage (2 min)**: `git status`, `git log --oneline -10`. Identify the last checkpoint where the app ran. State what broke in one sentence.
2. **Stabilize**: if the current state is not fixable in 10 minutes, `git stash` and restore the last green checkpoint. Do not debug while the clock burns.
3. **Protect the submission floor** (a submitted partial project beats an unsubmitted perfect one). Guarantee, in this order: public repo with pushed commits; a live deployed URL that loads (offline mode is acceptable and must be labeled); a 120-150 word honest description; the Gen AI services register matching what the code really calls; a demo video of whatever works. Each of the six requirements must be satisfiable.
4. **Cut line**: list what is cut using the cut order in `05-time-and-scope.md`. Never cut Layer 1 guardrails, telemetry, the visible fallback, the Judge Bar or any submission requirement.
5. **Protect the demo**: make the preset run end to end on the deployed URL; if live mode is unreliable, demo offline mode honestly and say so.
6. **Re-plan**: output a new clock-time plan for the remaining minutes with the new freeze and submitted-by times, and tell `/pitch` what to drop.
7. Commit and push `checkpoint: rescue`; print the Auto-Pilot Box with the next command (usually `/submit`).
