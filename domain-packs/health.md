---
domain: health
description: Clinical safety disclaimers, triage escalation and PII scrubbing.
---

# Health Pack

1. Banner: *"Clinical Decision Support Prototype - Does not replace professional diagnosis."*
2. Emergency escalation: severe symptoms trigger an immediate red alert modal with a call-emergency-services instruction.
3. Entities: patient (anonymized), symptoms, history, vitals. Output: triage level, rationale, next steps.
4. Grounding: cite guideline names or provided records only; never fabricate dosages.
5. PII masking: anonymize names to `PT-2026-XXX`; strip phone, address, IDs.
6. Judge Preset: a case with one red-flag symptom hidden among routine ones.
7. Tests: dosage-diagnosis demand (out of scope), PII in free text, contradictory vitals.
