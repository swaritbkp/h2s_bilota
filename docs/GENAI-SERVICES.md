# Gen AI Services Register

Continuously maintained register of all Gen AI services called in code. Evaluators and organizers can verify each call site directly.

| Service / Model | Purpose | Where in Code (`file:function`) | Where User / Judge Sees It | Live or Fallback |
|---|---|---|---|---|
| **Google Gemini (`gemini-2.5-flash`)** | Vernacular gig-shift intake parsing, statutory welfare reasoning (e-Shram / PM-JAY / State Boards), and legal grievance notice generation | `src/agent/agent.py:call_gemini_reasoning` | Main 4-Pillar Copilot Dashboard, Anomaly Alert Card, Grievance Letter, and Live Telemetry Drawer | Live Google GenAI API with automatic 2500ms timeout fallback to verified civic benchmark models |

---

### Verification Command
Run this command to verify all GenAI service call sites across the codebase:
```bash
git grep -nE "GENAI-SERVICE|google\.genai|gemini"
```
