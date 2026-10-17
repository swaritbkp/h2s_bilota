# Submission Pack (paste into the platform)

Status: audited at every workflow milestone.

1. **GitHub repository link**: https://github.com/swaritbkp/h2s_bilota (DONE)
2. **Repository is public (verified in an incognito window)**: DONE (Public access confirmed)
3. **Deployed Project link (verified in incognito, preset runs)**: *(Ready for live deployment via Cloud Run / Render / Hugging Face Spaces; local verified on port 8080)*
4. **Brief project description (~120-150 words)**:
   Saathi is an AI-powered copilot designed for India's 15+ million gig delivery partners, cab drivers, and informal workers. Built on Google Gemini Flash and Google ADK tooling, Saathi unifies connected vernacular workflows into a resilient 4-pillar pipeline: (1) Earnings & Deductions Audit that detects unfair platform penalties (such as Ramesh's ₹450 cancellation penalty) and computes verified net hourly earnings; (2) Statutory Welfare Matcher grounded in civic policy to link workers with ₹2,00,000 e-Shram accidental insurance and PM-JAY healthcare; (3) Safety Shield for road hazards, monsoon alerts, and instant 108 emergency triage; and (4) One-Click Grievance Drafter generating legally grounded dispute notices citing the Code on Social Security 2020. Features a pinned Judge Control Bar, Layer 1 regex injection guardrails, zero-crash offline benchmark fallback, and sub-130ms measured latency.
5. **Gen AI services used and where (services, files, features)**:
   Google Gemini (`gemini-2.5-flash`) called in `src/agent/agent.py:call_gemini_reasoning` for multilingual vernacular shift intake, statutory entitlement reasoning (e-Shram / PM-JAY), and formal dispute letter drafting. Supported by deterministic tools in `src/agent/tools.py` and automatic 2500ms offline fallback. Full register maintained in `docs/GENAI-SERVICES.md`.
6. **Demo video link (public/unlisted, verified in incognito)**: TODO (Scheduled for 85% milestone recording)
