---
name: grounding
description: Factual attribution, citations, deterministic grounding score and the human-review path.
---

# Skill: Grounding & Anti-Hallucination

- Every factual claim carries a citation id: `[Verified Data]` (traceable to an input or source) or `[Calculated Formula]` (a calculation id).
- `groundingConfidence` = supported claims / total claims, computed in code. Never ask the model to rate itself.
- Badges: `High: 95%+`, `Medium: 75-94%`, `Needs Review: <75%`. Needs Review outputs are routed to the human-review state in the UI.
- Never invent a metric. If an input is missing, say "Insufficient data" and list what is missing.
- For retrieval: cite document id plus span; reject claims whose cited span does not support them.
