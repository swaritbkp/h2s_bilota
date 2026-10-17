---
name: genai-register
description: Keeps an accurate register of every Gen AI service used and where, so submission requirement 5 is satisfied.
---

# Skill: Gen AI Services Register

Official requirement: clearly mention which Gen AI services were used and where in the submission.

1. The moment a Gen AI service is called in code, add a row to `docs/GENAI-SERVICES.md`: service/model, purpose, where in code (`file:function`), where the user sees it (screen/feature), live or fallback.
2. Tag the call site: `GENAI-SERVICE: <service/model> | <purpose>` as a code comment.
3. Include everything: ADK agent runtime, Gemini model(s), embeddings, speech/vision/image services, any other Gen AI API. Deterministic code and mock data are NOT Gen AI; do not list them.
4. Take model IDs from the code or `.env`, never from memory. If a call falls back to sample data, say so in the "Live or fallback" column.
5. `/submit` verifies the register with a search of the code for imports and calls (for example `git grep -nE "google\.adk|google\.genai|vertexai|gemini"`) and reconciles it with the tags.
6. Reuse the same table in the README ("Gen AI Services Used") and a one-line summary in the platform description.
