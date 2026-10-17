---
name: domain-binder
description: Binds an existing domain pack or creates a new one from the template when the problem is in an unfamiliar domain.
---

# Skill: Domain Binder

1. Match the problem to a pack in `domain-packs/`. If one fits, bind it.
2. If none fits, copy `domain-packs/_template.md` to `domain-packs/<new-domain>.md` and fill: compliance/disclaimer line, numeric and unit rules, key entities and output schema, trusted source types for grounding, PII rules, preset design with ONE actionable anomaly, and 3 domain-specific attack/out-of-scope test cases.
3. Record the binding in `docs/KICKOFF.md`.
4. Never copy finance-specific assumptions (currency, risk language) into a non-finance domain.
