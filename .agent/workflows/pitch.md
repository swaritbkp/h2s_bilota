---
description: Timed stage script (2 or 5 minutes), slide outline and 7-question Judge Defense Matrix.
---

# Workflow: `/pitch`

Use the pitch length announced at kickoff. Every number is tagged `[MEASURED]`, `[SOURCED]` or `[ESTIMATE]`. The demo runs on the DEPLOYED URL, with the preset one click away.

Generate `PITCH_SCRIPT.md`:

**2-minute structure**
- `[0:00 - 0:20]` Hook: one person, one moment, quantified friction.
- `[0:20 - 1:20]` Live demo: preset -> result -> telemetry drawer.
- `[1:20 - 1:45]` Mic drop: injection attack, live rejection, name the layer that caught it.
- `[1:45 - 2:00]` One line on the Gen AI services used, one line on scale/govern/optimise, then the impact line.

**5-minute structure**
- `[0:00 - 0:45]` Hook and quantified friction.
- `[0:45 - 2:15]` Live demo: preset -> agent result -> telemetry.
- `[2:15 - 3:00]` Mic drop: injection attack and live rejection.
- `[3:00 - 4:00]` Under the hood: architecture, ADK + Gemini (name the exact services), measured results if any.
- `[4:00 - 4:40]` Scale / Govern / Optimise in three lines.
- `[4:40 - 5:00]` Impact line and the ask.

Also generate:
1. `docs/SLIDES.md`: 5 to 7 slides max (problem, solution, demo cue, architecture + Gen AI services, guardrails, scale/govern/optimise, impact).
2. `docs/JUDGE-QA.md`: crisp 2-3 sentence answers with repo evidence for: hallucination, latency, offline resilience, why not just ChatGPT, scaling to 100x, governance and versioning, business model / next month.

The demo video is produced by `/submit` (`docs/DEMO-VIDEO.md`); reuse its click path so the live demo and the video match. Print the Auto-Pilot Box: next action is two timed rehearsals and `docs/DEMO-DAY-CHECKLIST.md`.
