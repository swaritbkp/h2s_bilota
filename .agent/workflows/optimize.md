---
description: Builds the working app, Judge Control Bar, 3 ADK tools and offline-safe demo mode, and gets a PUBLIC deployed skeleton live by 30% of build time.
---

# Workflow: `/optimize`

When triggered:
1. Read `docs/KICKOFF.md`. Respect constraints, negative scope and the six submission requirements.
2. Create the structure: `src/core/` (UI-independent `analyze`, guardrails, grounding), `src/agent/` (Google ADK agent + 3 tools), `src/ui/` (front end), `prompts/agent/` (agent prompt with canary).
3. Implement the agent with Google ADK + Gemini (see `adk-agent` skill). Deterministic logic in code; the LLM reasons and narrates only.
4. Tag every Gen AI call site with `GENAI-SERVICE: <name> | <purpose>` and add its row to `docs/GENAI-SERVICES.md` immediately.
5. Wire the Judge Control Bar per `30-judge-bar-and-fallback.md` with the visible offline fallback and a no-API-key offline mode.
6. Implement the Result contract (`20-eval-contract.md`). The eval adapter is optional in LEAN.
7. Create a judge-facing `README.md` stub (project name, one-line problem, how to run, "Gen AI Services Used" placeholder, links placeholder).
8. **Deploy a skeleton to a public URL as soon as the first end-to-end slice runs locally (target: 30% of build time).** The Gemini key is server-side only. Verify the URL in an incognito window. Record it in `docs/SUBMISSION.md`.
9. Apply `ui-polish`. Verify zero console errors and that the preset runs in live and offline mode, locally and on the deployed URL.
10. Create the Layer 1 guardrail now. Commit and push `checkpoint: optimize`; print the Auto-Pilot Box with the `/guardrails` command.
