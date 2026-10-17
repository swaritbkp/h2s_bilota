# PromptWars Elite Pack v2.1 - Pack Guide

Event: Google for Developers x Hack2skill PromptWars (in-person, vibe coding). The problem is revealed at the venue, you build from scratch, and top builders pitch live to industry experts the same day. Judged on intent, speed and execution.

This guide is for the team. The `README.md` in your repo is for judges: `/optimize` creates a stub and `/deploy` finalizes it.

## The 6 Official Submission Requirements
1. GitHub repository link submitted on the platform.
2. The repository is published and set to PUBLIC access.
3. "Deployed Project" link submitted on the platform.
4. Brief description of the project built.
5. Clearly mention which Gen AI services were used AND where in the submission.
6. Project demo video link for evaluators to review.

Confirm exact field names, limits and the deadline with the organizers at the venue.

## Pipeline (default depth: LEAN)
| # | Command | What it does | Output |
|---|---------|--------------|--------|
| 1 | `/kickoff` | The six requirements + constraints FIRST, then decode, plan | `docs/KICKOFF.md` |
| 2 | `/optimize` | Build app, Judge Bar, tools; first PUBLIC deploy by 30% of build time | working app + live URL |
| 3 | `/guardrails` | Injection defense + manual attack tests (measured eval only if time) | `docs/GUARDRAIL-NOTES.md` |
| 4 | `/scale` | Scale / Govern / Optimise: architecture doc + slide (code only in FULL) | `docs/ARCHITECTURE.md` |
| 5 | `/deploy` | Redeploy, secret scan, judge README, freeze tag | `demo-freeze` tag |
| 6 | `/submit` | Audit all 6 requirements, Gen AI register, demo video, paste-ready pack | `docs/SUBMISSION.md` |
| 7 | `/pitch` | Timed script (2 or 5 min), slides, Judge Q&A | `PITCH_SCRIPT.md` |
| - | `/rescue` | Anytime: revert, cut, protect the submission floor | rescue plan |

Say `Depth: FULL` in `/kickoff` to enable the heavy layers (L2 classifier, measured eval harness, prompt versioning, scale code). For a one-day vibe-coding event, stay LEAN.

## Golden Rules
1. The six requirements outrank everything. Target: submitted by 92% of build time.
2. Public repo from minute one. Push after every checkpoint. NEVER commit secrets (the repo is public).
3. Deploy a skeleton to a public URL by 30% of build time; redeploy at every checkpoint.
4. Every Gen AI service is registered in `docs/GENAI-SERVICES.md` the moment it is used.
5. Every number you say is MEASURED, SOURCED or ESTIMATE. Fallback is always visible.
6. Feature freeze at 70%, demo freeze at 85%.
7. A submitted partial project beats an unsubmitted perfect one.

## Folder Map
- `.agent/rules/`      always-on behavior (core, time, guardrails, eval contract, judge bar, submission)
- `.agent/workflows/`  the slash commands above
- `.agent/skills/`     reusable expertise (incl. `genai-register`)
- `domain-packs/`      domain adaptors + `_template.md`
- `prompts/`           copy-paste commands, spec template, versioned agent prompts
- `eval/`              `run_eval.py` (measured harness, optional) + attack suite starter
- `docs/`              kickoff, submission pack, Gen AI register, architecture, checklist

## Day-of Setup (5 minutes)
1. Open this folder as the workspace in Antigravity; confirm the rules are always-on.
2. Create a PUBLIC GitHub repo; keep the URL ready for `/kickoff`.
3. Copy `.env.example` to `.env`, add your key, make one real Gemini call to confirm it works.
4. Open `prompts/PROMPTS.md` and paste Step 1 with the problem statement.
