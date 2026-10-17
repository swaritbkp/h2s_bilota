---
description: Audit and assemble all 6 official submission requirements, verify them from an incognito view, and produce a paste-ready submission pack.
---

# Workflow: `/submit`

Run when `/deploy` is done (target: complete by 92% of build time). Update `docs/SUBMISSION.md` as you go; mark each item DONE or MISSING with evidence.

1. **Repository (req 1-2)**: confirm `origin` and that all commits are pushed. Ask the user to open the repo URL in an incognito window to confirm it is PUBLIC (or check with `curl -s -o /dev/null -w "%{http_code}" <repo-url>`: 200 means public). Run the secret scan: `git ls-files | grep -E "^\.env$"` must be empty; `git grep -nE "AIza[0-9A-Za-z_-]{20,}"` must be empty; `git log --all -p -S"AIza" --oneline | head` must be empty. If anything is found: remove it and tell the user to rotate the key.
2. **Deployed project (req 3)**: verify the URL returns 200, loads in incognito with no login, the Judge Preset runs on it, and offline mode works with no key. Check the built bundle does not contain the API key.
3. **Description (req 4)**: write about 120-150 words: who suffers, what we built, how it works, Gen AI services used, repo and deployed links. No unmeasured claims.
4. **Gen AI services (req 5)**: run the `genai-register` audit: search the code for Gen AI imports and calls, reconcile with `GENAI-SERVICE:` tags and `docs/GENAI-SERVICES.md`, remove placeholder rows. Make sure README has a "Gen AI Services Used" section with file paths and the description names the services.
5. **Demo video (req 6)**: write `docs/DEMO-VIDEO.md` (90-second script with exact click path on the DEPLOYED URL, voiceover lines, the 5-second on-screen Gen AI services card, recording checklist). The user records and uploads (YouTube unlisted or Drive "Anyone with the link"). Verify the link opens in incognito and the video length meets the limit.
6. **Output the Submission Pack** in `docs/SUBMISSION.md` as copy-paste fields in the platform's order (repo link, public confirmation, deployed link, description, Gen AI services, video link), with each item's status.
7. Tell the user exactly which items are still MISSING and the fastest way to close each. If time is short, close them in this order: repo public, deployed link, description, Gen AI services, video.
8. Commit, push, tag `submitted-candidate`. Print the Auto-Pilot Box: the next action is pasting the pack into the platform and submitting, then `/pitch` rehearsal.
