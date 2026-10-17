---
description: Injection defense and attack testing. LEAN: Layer 1 + canary + manual attack tests. FULL: layered defense with the measured eval harness.
---

# Workflow: `/guardrails`

## LEAN (default)
1. Implement Layer 1 (normalize, clamp, strip, pattern match), the canary check and basic output schema validation per `10-guardrails.md`.
2. Test by hand through the Judge Bar attack button and the 5 attack inputs in `eval/test-suite.example.json` (direct, paraphrased, zero-width obfuscated, prompt-leak, out-of-domain). Run them on the DEPLOYED build too.
3. Write what actually happened (observed only) to `docs/GUARDRAIL-NOTES.md`: input, layer that caught it, result. Never claim an unobserved result.
4. Fix failures. If more than 30% of build time remains, continue with FULL.

## FULL (`Depth: FULL`, or time remains)
1. Create `eval/test-suite.json` from `eval/test-suite.example.json`; replace every `todo` case with real domain cases (happy path, offline fallback, domain PII, out-of-scope).
2. Implement L2 classifier, L3 output validation and PII scrub per `10-guardrails.md`.
3. Run the real harness: `python eval/run_eval.py --mode <http|cmd> --target "<url or command>"`. Never hand-write results. Keep the first run as the BEFORE snapshot.
4. Patch failures; if the prompt changes, create `prompts/agent/system.v2.md`, register it, bump `promptVersion`. Re-run until all executed cases pass; record before/after in `eval/benchmark-report.md` and `prompts/agent/VERSIONS.md`.

Finish: commit and push `checkpoint: guardrails`; print the Auto-Pilot Box with the `/scale` command.
