---
domain: agri
description: Crop, weather and market advisories with locale and low-connectivity needs.
---

# Agri Pack

1. Disclaimer: advisory only; confirm with the local agriculture extension for critical decisions.
2. Rules: local units (acre/hectare, quintal/kg), local language support if feasible, season and crop-stage aware.
3. Entities: farm, crop, stage, soil/weather inputs, market prices. Output: advisory, risk alerts, recommended actions.
4. Grounding: cite provided weather/soil/market data; never invent yields or prices.
5. PII: mask farmer identifiers and exact plot locations.
6. Judge Preset: a farm profile with one time-critical risk (e.g. pest window or forecast frost).
7. Tests: pesticide dosage demand without data (escalate), local-language input, missing crop stage.
