---
name: adk-agent
description: Builds the agent with Google ADK + Gemini: three deterministic tools, timeouts, telemetry, structured output.
---

# Skill: ADK Agent Tooling (Google Agent Development Kit + Gemini)

Verify the installed ADK package and its docs before writing code. Do not guess signatures.

## Shape
- Start with ONE agent plus function tools. Add sub-agents only if the problem clearly needs delegation, and be ready to explain why.
- Model tiering: Flash-class by default; Pro-class only for the single step that needs deeper reasoning. Record the choice for `/scale`.
- Deterministic work (math, validation, lookups) is plain code inside tools. The LLM reasons, explains and orchestrates.
- Use structured output (response schema / JSON schema) for every model call that feeds code.

## Three tools (generic names; rename to the domain)
1. `ingest_and_validate`: normalize and validate input, run guardrail Layers 1-2, wrap untrusted data.
2. `compute_and_ground`: run domain logic and attach citations; compute `groundingConfidence` deterministically.
3. `export_decision_artifact`: produce the final structured report / action plan.

## Reliability
- Each tool races `TOOL_TIMEOUT_MS`; on failure use the visible offline fallback (`fallbackUsed: true`).
- Pre-warm the model client on load.
- Emit telemetry for every tool call:
```json
{
  "toolName": "compute_and_ground",
  "status": "PASS",
  "durationMs": 35,
  "groundingConfidence": 0.98,
  "fallbackUsed": false,
  "promptVersion": "v1",
  "agentVersion": "1.0.0"
}
```
