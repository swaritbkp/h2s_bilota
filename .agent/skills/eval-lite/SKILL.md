---
name: eval-lite
description: Runs the real eval harness, interprets results, and drives before/after improvement. Never hand-writes numbers.
---

# Skill: Eval-Lite Runner

The harness is `eval/run_eval.py` (stdlib only). It calls the app via HTTP or CLI, validates the Result contract and writes `eval/benchmark-report.md` and `eval/results.json`, plus a snapshot in `eval/history/`.

```text
python eval/run_eval.py --mode http --target http://localhost:8000/api/analyze
python eval/run_eval.py --mode cmd  --target "python -m app.cli"
```

Checks per case: schema validity, allowed status, required output keys, citations, minimum grounding, latency budget, forbidden strings (canary / prompt leaks) and expected fallback behavior.

Rules:
- Never edit the report by hand. If a number is not in the report, it does not go on a slide.
- `todo` cases are reported as SKIPPED; replace them with real cases before the final run.
- Loop: run -> read failures -> patch -> bump prompt version if the prompt changed -> run again. Keep BEFORE and AFTER numbers.
