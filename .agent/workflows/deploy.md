---
description: Redeploy to the public URL, secret scan, judge-facing README, freeze tag.
---

# Workflow: `/deploy`

When triggered:
1. Run the production build/lint. Zero broken imports, zero console warnings.
2. Redeploy the latest build to the PUBLIC deployed URL. Verify in an incognito window: loads without login, Judge Preset runs, injection button works, offline mode works with no key.
3. Secret safety (the repo is public): `.env` is not tracked, `.env.example` is complete, no key in the code, git history or built bundle (`git grep -nE "AIza[0-9A-Za-z_-]{20,}"`). If a key leaked: remove it and rotate it.
4. Finalize the judge-facing `README.md`: problem and who suffers, solution, architecture diagram, how to run, guardrails summary, **Gen AI Services Used (table with file paths, from `docs/GENAI-SERVICES.md`)**, deployed URL, demo video URL (placeholder until `/submit`), honest limitations. One line noting it was built with Google Antigravity (vibe coding).
5. If time remains (more than 15% of build time): fresh `git clone` into a temp folder, install, run from the README alone.
6. If the eval harness was used, run it one last time.
7. Commit and push, then `git tag demo-freeze && git push --tags`. Print the Auto-Pilot Box with the `/submit` command.
