---
name: versioning
description: Prompt versioning, agent versioning, registry, rollback and changelog with measured results.
---

# Skill: Versioning (prompts, agent, changelog)

- Prompts live in `prompts/agent/system.vN.md`. The active one is set in `prompts/agent/registry.json` (`active`). Rolling back = changing that pointer.
- `agentVersion` is semantic (`1.0.0`). Bump minor when tools or flow change, patch for fixes.
- Every bump records in `prompts/agent/VERSIONS.md`: version, date, reason, `[MEASURED]` pass rate, latency and grounding before/after.
- `promptVersion` and `agentVersion` appear in every telemetry object, the audit log and the UI footer.
- Append a `CHANGELOG.md` entry per workflow milestone: date, components changed, measured pass rate.
- Never change a prompt without re-running `eval/run_eval.py`.
