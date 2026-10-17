# 90-Second Demo Video Script & Recording Guide

This document provides the exact click path, timed voiceover script, and recording checklist for the evaluator demo video (Submission Requirement 6).

---

## ⏱️ Timed 90-Second Video Script

| Timecode | Visual / On-Screen Action | Spoken Voiceover Line |
|---|---|---|
| **00:00 - 00:15** | Open the live deployed Saathi web application. Show the title and dark slate interface. | *"Over 15 million gig workers in India lose up to ₹3,500 every month to opaque platform penalties and fuel deductions, while missing out on statutory rights like e-Shram accident insurance. Meet Saathi — a multilingual GenAI copilot built for India's informal workforce."* |
| **00:15 - 00:45** | Click the pinned **`⚡ Load Judge Preset (Ramesh)`** button in the Judge Control Bar. | *"In one click, Saathi ingests Ramesh's 12-hour Hinglish shift report and executes a connected 4-pillar pipeline. **Pillar 1** audits his earnings, flagging an unexplained ₹450 penalty deduction that dropped his net wage to ₹62.50 an hour. **Pillar 2** grounds his case in civic policy, discovering he is eligible for ₹2 Lakh accidental insurance under e-Shram. **Pillar 3** triages monsoon road hazards with rapid 108 emergency dials. And **Pillar 4** automatically generates a platform compliance dispute notice citing Sections 112 to 114 of the Code on Social Security 2020."* |
| **00:45 - 01:05** | Click **`📋 Copy Dispute Notice`** (show "Copied to clipboard! ✓" toast). Then click the **`🚗 Sample: Ola/Uber Driver`** pill and hit Run. | *"Notice how the pipeline is fully dynamic. When we switch to an Ola/Uber cab driver facing ₹1,100 fuel expenses and ₹650 commission over a 14-hour Delhi shift, the audit, fatigue alerts, and legal notice instantly adapt to the driver's specific scenario. Workers can copy this formal letter with one tap."* |
| **01:05 - 01:15** | Click the pinned **`💥 Test Injection Attack`** button in the Judge Control Bar. Open the **`🧠 Agent Telemetry`** drawer. | *"Saathi is enterprise-hardened. When an adversary attempts a prompt injection attack, our Layer 1 deterministic shield blocks it in zero milliseconds without leaking our canary token or touching the LLM. Telemetry displays live latency, grounding confidence, and active defense layers."* |
| **01:15 - 01:22** | **[MANDATORY 5-SECOND CARD]** Display the Gen AI Services Used table on screen. | *"Saathi is powered by Google Gemini Flash via the Google GenAI SDK in `src/agent/agent.py`, backed by deterministic mathematical tools and a zero-crash offline benchmark fallback."* |
| **01:22 - 01:30** | Return to the Saathi Copilot dashboard and show Presenter Mode. | *"Saathi turns complex labor law and chaotic shift notes into instant financial justice and social security for India's informal workers. Built with Google Antigravity for PromptWars."* |

---

## 🎬 5-Second On-Screen Gen AI Services Card (Freeze Frame at 01:15)

Show this table or graphic clearly on screen:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        GEN AI SERVICES USED                            │
├────────────────────────────────────────────────────────────────────────┤
│ • Model: Google Gemini (gemini-3.8-flash) via Google GenAI SDK         │
│ • Call Site: src/agent/agent.py : call_gemini_reasoning               │
│ • Purpose: Multilingual shift extraction & formal legal drafting       │
│ • Resilience: Sub-second timeout with verified offline civic fallback │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📹 Video Production & Submission Checklist

- [ ] **Recording Resolution**: 1080p (1920x1080) at 30 or 60 fps.
- [ ] **Audio Quality**: Clear voiceover without background venue noise.
- [ ] **Duration**: Exactly 75 to 90 seconds (never exceeds 120 seconds).
- [ ] **Environment**: Screen recording on the deployed public URL (or local app in fullscreen browser).
- [ ] **Upload Setting**:
  - YouTube: Set to **Unlisted** (or Public).
  - Google Drive: Set to **"Anyone with the link can view"**.
- [ ] **Verification**: Open the video link in a **private / incognito window** to confirm evaluators can watch without logging in.
- [ ] **Submission**: Paste the verified link into Field 6 of [`docs/SUBMISSION.md`](file:///c:/Users/S/OneDrive/Desktop/WarmupSesson/docs/SUBMISSION.md).
