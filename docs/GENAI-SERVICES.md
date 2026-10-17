# Gen AI Services Register

Update the moment a service is used. List only services the code actually calls.

| Service / model | Purpose | Where in code (file:function) | Where the user sees it | Live or fallback |
|---|---|---|---|---|
| Google Gemini (`gemini-2.5-flash`) | Operational diagnostic reasoning, scoring formula verification, and strategy recommendations | `src/core/engine.py:analyze` | Main diagnostic analysis card, scoring breakdown, and recommendations | Live with automatic offline benchmark fallback |
