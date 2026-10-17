---
name: time-and-scope
description: Phase budget with deploy-early milestones, feature freeze, demo freeze, submitted-by target, cut order.
---

# Time & Scope Rules

Total build time = T (ask in `/kickoff`; if unknown, assume 4 hours). Convert to clock times in `docs/KICKOFF.md`.

| Phase | Share of T | Workflow |
|-------|-----------|----------|
| Decode & plan | 0-8% | `/kickoff` |
| Build (first PUBLIC deploy by 30%) | 8-48% | `/optimize` |
| Harden | 48-60% | `/guardrails` |
| Scale / Govern / Optimise (docs only in LEAN) | 60-68% | `/scale` |
| Deploy & freeze | 68-78% | `/deploy` |
| Submission package + demo video | 78-92% | `/submit` |
| Pitch script and rehearsal (parallel) | 80-100% | `/pitch` |

Milestones:
- **30% of T**: skeleton deployed to a public URL and the public repo has pushed commits.
- **70% of T: feature freeze.** After this: fixes only.
- **85% of T: demo freeze.** Only show-stopper fixes. Demo video recorded by this point.
- **92% of T: SUBMITTED.** Final polish happens only after the submission is in (update it if the platform allows).
- If a phase overruns by more than 25%, run `/rescue`.

## Scope Discipline
- Happy path first. One "wow" feature, maximum.
- Cut order when behind: extra screens > tools beyond 3 > animations > secondary integrations > polish > L2/L3 guardrails and eval harness > everything else. Never cut: Layer 1 guardrails, telemetry, visible fallback, the Judge Bar, or any of the six submission requirements.
- Negative scope from `docs/KICKOFF.md` is binding.
- Confirm the platform's real submission deadline with the organizers; if it is earlier than the pitch, move every milestone earlier.
