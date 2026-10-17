---
description: The 6 official submission requirements and constraints FIRST, then decode the problem, bind a domain pack, define the contract and a clock-time plan. LEAN by default.
---

# Workflow: `/kickoff`

Expected in the user's message: problem statement, total build time, pitch length, team size, the PUBLIC GitHub repo URL, any announced judging criteria or mandated tech, and optionally `Depth: FULL`. If total build time is missing, ask ONE question for it; assume the rest and state the assumptions. Default depth is LEAN.

When triggered, create `docs/KICKOFF.md` with these sections, in this order:
1. **Constraints & Submission Checklist** - pre-filled with the six official requirements from `40-submission-requirements.md`, plus any mandated tech and the deadline. Checkbox list. These outrank everything.
2. **Event Context** - in-person vibe-coding hackathon, judged on intent, speed and execution, live pitch for top builders the same day.
3. **Judging Criteria** - announced criteria verbatim. If none: Innovation 25 / Technical Depth 25 / Guardrails & Grounding 25 / Demo Polish 25, labeled `ASSUMED`.
4. **Core Friction** - 2 sentences, quantified; tag numbers `[SOURCED]` or `[ESTIMATE]`.
5. **3-Step Happy Path** - Input -> Agent Compute -> Deliverable.
6. **Hidden Criteria & Negative Scope** - what judges likely reward; what we will NOT build.
7. **Domain Binding** - ingest the matching `domain-packs/<name>.md`; if none fits, run the `domain-binder` skill.
8. **Contract** - the Result contract (`20-eval-contract.md`) plus the domain `output` schema.
9. **Clock-time Plan** - convert `05-time-and-scope.md` into real clock times: first public deploy (30%), feature freeze (70%), demo freeze (85%), SUBMITTED (92%).
10. **The One Wow** - the single differentiator and how it appears in the first 60 seconds of the demo.
11. **Submission Plan** - when each of the six requirements is produced (repo now, deployed skeleton by 30%, Gen AI register continuously, description draft by 60%, video by 85%).

Then: `git init` if needed; set `origin` to the public repo URL (if none was given, tell the user to create a PUBLIC repo and paste the URL); commit and push `checkpoint: kickoff`; print the Auto-Pilot Box with the exact `/optimize` command.
