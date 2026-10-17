# Master Copy-Paste Execution Commands

## Step 1: Kickoff
```text
/kickoff
Problem Statement: { PASTE_CHALLENGE_HERE }
Total build time: { e.g. 4 hours }
Pitch length: { e.g. 2 minutes }
Team size: { n }
Public GitHub repo URL: { https://github.com/... }
Mandated tech / judging criteria (if announced): { paste, or "none announced" }
Depth: LEAN
Idea brief (from my ideation prompts): { PASTE }
```

## Step 2: Build App, Judge Bar and first public deploy
```text
/optimize
Build the working app from docs/KICKOFF.md using Google ADK + Gemini. Judge Control Bar (⚡ Load Judge Preset, 💥 Test Injection Attack, 🧠 Agent Telemetry), 3 tools with visible offline fallback, tag every Gen AI call with GENAI-SERVICE and update docs/GENAI-SERVICES.md. Deploy a public skeleton as soon as the first slice works (target 30% of build time) and record the URL.
```

## Step 3: Guardrails
```text
/guardrails
LEAN: Layer 1 + canary + manual attack tests on the deployed build; write observed results to docs/GUARDRAIL-NOTES.md.
```

## Step 4: Scale / Govern / Optimise
```text
/scale
LEAN: docs/ARCHITECTURE.md and one slide only.
```

## Step 5: Production Lock
```text
/deploy
Redeploy to the public URL, verify in incognito, secret-scan the public repo, finalize the judge README with the Gen AI Services Used table, push and tag demo-freeze.
```

## Step 6: Submission
```text
/submit
Audit all 6 official requirements, write the description, reconcile the Gen AI register, write docs/DEMO-VIDEO.md, and give me the paste-ready submission pack.
```

## Step 7: Stage Pitch (can run in parallel with Step 6)
```text
/pitch
Pitch length: { 2 minutes }. Generate PITCH_SCRIPT.md, docs/SLIDES.md and docs/JUDGE-QA.md.
```

## Emergency: Rescue
```text
/rescue
Something is broken or we are behind. Revert to the last green checkpoint, protect the six submission requirements first, then the demo, and re-plan the remaining time.
```
