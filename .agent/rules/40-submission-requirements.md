---
name: submission-requirements
description: The six official PromptWars submission requirements, Definition of Done, and repo/deploy/Gen AI/video rules. Always on.
---

# Submission Requirements (official, non-negotiable)

| # | Official requirement | Our deliverable | Proof |
|---|----------------------|-----------------|-------|
| 1 | GitHub repository link submitted on the platform | Repo URL in `docs/SUBMISSION.md` | `git remote -v` shows it |
| 2 | Repository published and set to public access | Public repo | Opens in an incognito window |
| 3 | "Deployed Project" link submitted on the platform | Live public URL | Opens in incognito, preset runs |
| 4 | Brief description of the project built | ~120-150 word description | `docs/SUBMISSION.md` field 4 |
| 5 | Clearly mention which Gen AI services were used and where in the submission | Gen AI Services Used section + register | README + description + `docs/GENAI-SERVICES.md` |
| 6 | Project demo video link for evaluators to review | Public/unlisted video link | Opens in incognito |

Confirm exact field names, limits and the deadline with the organizers. If the wording differs from this table, the organizers' wording wins.

## Definition of Done
A submission is DONE only when all six are true AND verified from a logged-out / incognito browser. The `/submit` workflow audits this and marks each item DONE or MISSING.

## Public repo rules
- Create the GitHub repo PUBLIC at `/kickoff` (the user provides the URL; set it as `origin`). Push after every checkpoint: this is also your off-machine backup.
- The repo is public: NEVER commit secrets. `.env` stays ignored; only `.env.example` is committed. Keys live in the hosting platform's environment/secret settings. If a key was ever committed, rotate it immediately.
- `README.md` is written for judges: what and why, how to run, architecture, Gen AI Services Used (with file paths), deployed URL, demo video URL, honest limitations.

## Deployed project rules
- Public URL, no login, works in incognito, and loads even with no API key (visibly labeled OFFLINE MODE).
- Deploy a skeleton by 30% of build time and redeploy at every checkpoint. Use the hosting the event provides; otherwise the fastest of Cloud Run, Firebase Hosting or another free tier. Do not spend more than 15 minutes choosing.
- The Gemini key is server-side only, never in browser code. Add a basic per-client rate limit so a public URL cannot burn the quota.
- The Judge Preset must run on the DEPLOYED URL, not just locally.

## Gen AI services rules
- Maintain `docs/GENAI-SERVICES.md` continuously (see the `genai-register` skill).
- Tag every call site with a comment: `GENAI-SERVICE: <service/model> | <purpose>`.
- State the services in three places: the platform description (one line), the README (section "Gen AI Services Used" with file paths), and `docs/GENAI-SERVICES.md` (full table).
- Only list services actually called in code. Verify model IDs from code/config, never from memory.

## Demo video rules
- 60-120 seconds (confirm the limit). Screen recording with voiceover: problem (10s) -> live demo on the DEPLOYED URL with the preset -> injection attack blocked -> Gen AI services used shown on screen for 5 seconds -> impact line.
- Host on YouTube (unlisted) or Google Drive ("Anyone with the link"). Open the link in incognito to verify before submitting.
- Record a first take by 80% of build time, even if rough. Re-record only if time remains.

## Description rules
About 120-150 words unless the platform limits it: who suffers, what we built, how it works in one line, Gen AI services used, links to the repo and the deployed project. No unmeasured claims.
