# Gen AI Services Register

Continuously maintained register of all Gen AI services called in code. Evaluators and organizers can verify each call site directly.

| Service / Model | Purpose | Where in Code (`file:function`) | Where User / Judge Sees It | Live or Fallback |
|---|---|---|---|---|
| **Google Gemini (`gemini-2.5-flash` / `gemini-2.0-flash` / `gemini-3.8-flash`)** | Dynamic vernacular gig-shift extraction, civic welfare reasoning (e-Shram / PM-JAY / State Boards), and legal grievance notice generation | `src/agent/agent.py:call_gemini_reasoning` | Main 4-Pillar Copilot Dashboard, Anomaly Alert Card, Grievance Letter, and Live Telemetry Drawer | Live Google GenAI API with automatic cascade and sub-50ms hybrid engine fallback |

---

### Verification Command
Run this command to verify all GenAI service call sites across the codebase:
```bash
git grep -nE "GENAI-SERVICE|google\.genai|gemini"
```
