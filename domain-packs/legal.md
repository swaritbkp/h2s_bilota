---
domain: legal
description: Clause analysis and risk flagging with strict non-advice framing.
---

# Legal Pack

1. Banner: *"Legal Information Prototype - Not Legal Advice. Consult a qualified lawyer."*
2. Rules: quote clause spans exactly, flag risk with a reason and severity, never assert jurisdiction-specific outcomes without the provided text.
3. Entities: document, clause, party, obligation, deadline, risk. Output: summary, flagged clauses, questions to ask counsel.
4. Grounding: every flag cites the clause span; no invented case law or statutes.
5. PII: mask party names and identifiers on export.
6. Judge Preset: a contract with one buried unfavorable clause.
7. Tests: "will I win this case" (out of scope), clause missing from the text, scanned-garbage input.
