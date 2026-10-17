---
name: problem-decoder
description: Turns a problem brief into constraints, a 3-step happy path, judging criteria, negative scope and a JSON contract.
---

# Skill: Problem Decoder

Extract, in this order:
1. Hard constraints and the submission checklist (mandated tech, deliverables, deadline).
2. Judging criteria: announced ones verbatim, else the `ASSUMED` rubric (Innovation 25, Technical Depth 25, Guardrails & Grounding 25, Demo Polish 25).
3. Core pain in 2 sentences, quantified; tag numbers `[SOURCED]` or `[ESTIMATE]`.
4. 3-step happy path: Ingest -> Reason -> Actionable Deliverable.
5. Hidden criteria (what a judge secretly rewards: clarity, realism, a real user, evidence) and Negative Scope (features to skip).
6. The One Wow, and how it appears in the first 60 seconds of the demo.
7. Strict JSON schema for the domain `output` field.

Think like an operator, not a coder: find the latent friction in the process first, then pick the simplest scalable solution that removes it.
