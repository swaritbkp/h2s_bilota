---
name: ui-polish
description: Stage-ready UI: dark slate theme, Judge Bar, projector legibility, all states handled.
---

# Skill: Stage-Ready UI Polish

1. Dark slate theme (`#0f172a`), emerald success badges, amber alerts (offline / needs review), red only for blocks.
2. Pin the Judge Control Bar at the top (see `30-judge-bar-and-fallback.md`).
3. Projector-safe: body text at least 16px, high contrast, nothing important in tiny type. Add a Presenter Mode toggle that scales text up.
4. Handle every state: empty, loading (skeleton), success, offline, blocked, error. No blank screens.
5. High-density cards, no dead white space, responsive layout.
6. Footer shows active `promptVersion` and `agentVersion`.
7. Zero console errors. Basic accessibility: labels, focus states, keyboard operable buttons.
