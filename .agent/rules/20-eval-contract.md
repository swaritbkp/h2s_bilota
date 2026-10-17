---
name: eval-contract
description: The Result contract and testable architecture so eval/run_eval.py can measure the app for real.
---

# Eval Contract (makes measured numbers possible)

## Architecture requirement
Core logic lives in a UI-independent module, e.g. `src/core/`, exposing one function:

`analyze(input) -> Result`

and (FULL depth, or LEAN if time allows) a thin adapter that the eval harness can call. Provide EITHER:
- **HTTP**: `POST /api/analyze` taking JSON, returning JSON, always HTTP 200 with a status field; OR
- **CLI**: a command that reads one JSON object from stdin and writes one JSON object to stdout (e.g. `python -m app.cli` or `node src/core/cli.js`).

The UI calls the same `analyze`. Nothing important may live only in the front end.

## Result contract (every response, including failures)
```json
{
  "status": "OK | GUARDRAIL_BLOCKED | OUT_OF_SCOPE | INVALID_INPUT | ERROR",
  "output": {},
  "citations": [{"id": "src-1", "label": "string", "kind": "Verified Data | Calculated Formula"}],
  "message": "human-readable note shown in the UI",
  "telemetry": {
    "toolName": "string",
    "status": "string",
    "durationMs": 0,
    "groundingConfidence": 0.0,
    "fallbackUsed": false,
    "promptVersion": "v1",
    "agentVersion": "1.0.0",
    "layers": {"L1": "PASS", "L2": "PASS | L2_SKIPPED | BLOCKED", "L3": "PASS"}
  }
}
```

## Test hooks
- Input flag `_simulateOffline: true` forces the fallback path (so eval can verify it).
- `analyze` never throws. Malformed input returns `INVALID_INPUT`.
- `groundingConfidence` is computed deterministically (supported claims / total claims), NOT self-reported by the model.
