---
name: scale-govern-optimise
description: Production-readiness story with real lightweight controls: scale, govern, optimise.
---

# Skill: Scale / Govern / Optimise

Judges reward teams that show what happens after the demo. Implement small real controls, then explain them.

## Scale
Stateless service, env-based config, container (Cloud Run style) deployment, horizontal scaling, in-memory cache for deterministic results (note Redis for multi-instance), per-client rate limit, queue for long jobs.

## Govern
Append-only audit log (`logs/audit.jsonl`), prompt/agent version registry with rollback, policy-as-code guardrails, PII handling, human-in-the-loop for `Needs Review`, clear ownership of who can change prompts and policies.

## Optimise
Measured latency and cost per request (tag `[MEASURED]` or `[ESTIMATE]` with assumptions), Flash vs Pro tiering, cache effect, eval-driven prompt iteration (v1 -> v2 delta).

Deliver `docs/ARCHITECTURE.md` with a diagram and a three-row table (Scale / Govern / Optimise: what we built, what we would add next).
