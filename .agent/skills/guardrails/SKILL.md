---
name: guardrails
description: Implements the layered guardrail module with policy-as-code, canary leak detection and clean UI rejection.
---

# Skill: Guardrails Shield

Implement `src/core/guardrails.*` following `10-guardrails.md`:
- L1 deterministic (normalize -> clamp -> strip -> pattern match), L2 Gemini classifier, L3 output validation with canary and PII scrub.
- Each layer returns `PASS | BLOCKED | L2_SKIPPED` into `telemetry.layers`.
- On a block: show a clean security toast, record `GUARDRAIL_BLOCKED`, never throw an unhandled error.
- Add unit tests for: direct injection, paraphrased injection, zero-width-obfuscated injection, script tag, prompt-leak request, oversized input, malformed input.
- Keep the policy list in one file so it can be versioned and audited (this is part of the Govern story).
