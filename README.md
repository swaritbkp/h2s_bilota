# PromptWars Elite Diagnostic System (`h2s_bilota`)

> **Google for Developers x Hack2skill PromptWars**  
> Operational Decision Support & Diagnostic Intelligence System.

---

## ⚡ Live Links & Resources
- **Public GitHub Repository**: [https://github.com/swaritbkp/h2s_bilota](https://github.com/swaritbkp/h2s_bilota)
- **Deployed Project URL**: *(Pending 30% milestone deploy during `/optimize`)*
- **Demo Video**: *(Pending 80% milestone recording during `/submit`)*

---

## 🛡️ Judge Control Bar & Interactive Functions
The app features a pinned top-level control bar built for live evaluator inspection:
1. **`⚡ Load Judge Preset`**: Instantly populates rich multi-tier operational telemetry with clear diagnostic bottlenecks.
2. **`💥 Test Injection Attack`**: Sends prompt injection and jailbreak payloads (`Ignore instructions...`) and displays real-time Layer 1 deterministic blocking.
3. **`🧠 Agent Telemetry`**: Collapsible drawer exposing live tool name, latency (ms), grounding confidence score, canary status, prompt/agent versions, and fallback telemetry.
4. **`⚡ OFFLINE MODE Badge`**: Amber indicator proving the app operates reliably with verified local benchmark models if external APIs or networks degrade.

---

## 🤖 Gen AI Services Used
| Service / Model | Call Site / File | Purpose |
| :--- | :--- | :--- |
| **Google Gemini (`gemini-2.5-flash`)** | [`src/core/engine.py`](file:///c:/Users/S/OneDrive/Desktop/WarmupSesson/src/core/engine.py) | Operational diagnostic assessment, root-cause bottleneck reasoning, and actionable strategy formulation. |

---

## 🚀 Running Locally
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
uvicorn src.app:app --host 0.0.0.0 --port 8080

# 3. Open in browser
http://localhost:8080
```

### Measured Eval Harness
```bash
python eval/run_eval.py --suite eval/test-suite.example.json --mode cmd --target "python src/cli.py"
```
