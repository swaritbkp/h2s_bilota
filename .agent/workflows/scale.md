---
description: Scale, Govern, Optimise story. LEAN: architecture doc and one slide. FULL: also lightweight real controls.
---

# Workflow: `/scale`

Goal: show judges this is more than a demo. Use the `scale-govern-optimise` skill.

## LEAN (default, about 10 minutes)
1. Write `docs/ARCHITECTURE.md`: a Mermaid or ASCII diagram, data flow, guardrail layers, and a three-row table (Scale / Govern / Optimise: what exists today, what we would add next).
2. Add one slide-ready summary to `docs/SLIDES.md`.
3. Only claim controls that really exist. Tag any cost or latency figure `[MEASURED]` or `[ESTIMATE]`.

## FULL (`Depth: FULL`, or time remains)
1. Scale: stateless service, in-memory cache for deterministic results, per-client rate limit, Cloud Run style deployment notes.
2. Govern: append-only audit log (`logs/audit.jsonl`), version display in the UI footer, human-review path for grounding below 75%.
3. Optimise: measure latency and cost per request; show Flash vs Pro tiering and the cache effect.
4. Re-run `eval/run_eval.py` if the harness is in use; nothing may regress.

Finish: commit and push `checkpoint: scale`; print the Auto-Pilot Box with the `/deploy` command.
