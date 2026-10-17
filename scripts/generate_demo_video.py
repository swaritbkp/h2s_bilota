"""Automated 60-Second Demo Video Generator for Saathi Copilot.

Uses Playwright headless Chromium to record a high-definition (1280x720) 60-second walkthrough
with step-by-step floating caption subtitles, demonstrating all 4 pillars, multi-platform presets,
Layer 1 injection security rejection, and agent telemetry.
"""

import os
import shutil
import subprocess
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Project Root & Video Output Directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "demo_video"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_URL = os.getenv("SAATHI_URL", "https://saathi-628506547347.asia-south1.run.app/")


def inject_subtitle_script(page):
    """Inject floating subtitle banner helper into the DOM."""
    script = """
    window.setDemoSubtitle = function(text) {
        let el = document.getElementById('demo-subtitle-banner');
        if (!el) {
            el = document.createElement('div');
            el.id = 'demo-subtitle-banner';
            el.style.position = 'fixed';
            el.style.bottom = '24px';
            el.style.left = '50%';
            el.style.transform = 'translateX(-50%)';
            el.style.background = 'rgba(15, 23, 42, 0.95)';
            el.style.color = '#38bdf8';
            el.style.border = '2px solid #38bdf8';
            el.style.padding = '12px 28px';
            el.style.borderRadius = '999px';
            el.style.fontSize = '18px';
            el.style.fontWeight = 'bold';
            el.style.fontFamily = "'Inter', -apple-system, sans-serif";
            el.style.zIndex = '99999';
            el.style.boxShadow = '0 10px 25px rgba(0,0,0,0.7)';
            el.style.textAlign = 'center';
            el.style.maxWidth = '92%';
            el.style.pointerEvents = 'none';
            el.style.transition = 'all 0.3s ease-in-out';
            document.body.appendChild(el);
        }
        el.textContent = text;
        el.style.display = 'block';
    };
    """
    page.evaluate(script)


def update_subtitle(page, text: str):
    """Set the active subtitle banner text."""
    print(f"  [Subtitle] {text}")
    page.evaluate(f"window.setDemoSubtitle({repr(text)})")


def smooth_scroll(page, target_y: int, duration_sec: float = 2.0, steps: int = 20):
    """Smoothly scroll the page to a target Y position."""
    current_y = page.evaluate("window.scrollY")
    distance = target_y - current_y
    step_duration = duration_sec / steps
    for i in range(1, steps + 1):
        intermediate_y = current_y + (distance * (i / steps))
        page.evaluate(f"window.scrollTo(0, {intermediate_y})")
        time.sleep(step_duration)


def run_demo_recording():
    print(f"🎬 Starting Saathi Copilot 60-second video recording on {TARGET_URL}...")

    # Clear old webm files in output directory
    for old_file in OUTPUT_DIR.glob("*.webm"):
        try:
            old_file.unlink()
        except Exception:
            pass

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--hide-scrollbars",
            ],
        )

        context = browser.new_context(
            record_video_dir=str(OUTPUT_DIR),
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720},
            device_scale_factor=1,
        )

        page = context.new_page()

        # Step 0: Open Target URL
        print("▶ Loading Saathi application...")
        page.goto(TARGET_URL, wait_until="networkidle", timeout=30000)
        inject_subtitle_script(page)

        # [0s - 6s] Intro Title
        update_subtitle(page, "Saathi Copilot: AI Assistant for 15M+ Indian Gig & Informal Workers (Built with Google Gemini)")
        time.sleep(6.0)

        # [6s - 15s] Scenario 1: Ramesh Delivery Preset
        update_subtitle(page, "Scenario 1: Ramesh (12h Swiggy/Zomato Shift) — Auditing ₹450 Unexplained Penalty")
        btn_preset = page.locator("#btn-preset, button:has-text('Load Judge Preset')").first
        if btn_preset.is_visible():
            btn_preset.click()
        else:
            page.locator("#pill-p1").first.click()

        # Wait for analysis rendering
        page.wait_for_timeout(4000)
        time.sleep(5.0)

        # [15s - 25s] Smooth Scroll to Pillars 1, 2, 3
        update_subtitle(page, "4-Pillar Pipeline: Wage Audit + Civic Welfare Matching + Monsoon Hazard Triage")
        smooth_scroll(page, target_y=450, duration_sec=3.0)
        time.sleep(7.0)

        # [25s - 35s] Pillar 4: Grievance Drafter & Language Toggle & Copy
        update_subtitle(page, "Pillar 4: Automated Legal Grievance Notice (Code on Social Security, 2020)")
        smooth_scroll(page, target_y=880, duration_sec=2.5)

        # Toggle Hindi if available
        btn_hi = page.locator("#btn-lang-hi").first
        if btn_hi.is_visible():
            btn_hi.click()
            time.sleep(2.0)

        # Toggle Bilingual
        btn_bi = page.locator("#btn-lang-bi").first
        if btn_bi.is_visible():
            btn_bi.click()
            time.sleep(2.0)

        # Click Copy Dispute Notice
        btn_copy = page.locator("#btn-copy, button:has-text('Copy')").first
        if btn_copy.is_visible():
            btn_copy.click()
            time.sleep(2.5)

        time.sleep(1.0)

        # [35s - 45s] Scenario 2: Dynamic Multi-Platform Dispute Analysis
        update_subtitle(page, "Scenario 2: Dynamic Multi-Platform Dispute Analysis (Uber/Ola & Quick-Commerce)")
        smooth_scroll(page, target_y=0, duration_sec=2.0)

        # Click Cab Driver (Rajesh 14h Uber fuel dispute)
        pill_cab = page.locator("#pill-p2, span:has-text('Rajesh')").first
        if pill_cab.is_visible():
            pill_cab.click()
            time.sleep(1.5)

        btn_run = page.locator("#btn-run, button:has-text('Run 4-Pillar')").first
        if btn_run.is_visible():
            btn_run.click()

        # Wait for dynamic result
        time.sleep(6.5)

        # [45s - 53s] Security Shield: Test Injection Attack
        update_subtitle(page, "Multi-Layer Security Shield: Real-Time Prompt Injection & PII Protection")
        btn_attack = page.locator("#btn-attack, #btn-injection, button:has-text('Test Injection Attack')").first
        if btn_attack.is_visible():
            btn_attack.click()

        time.sleep(7.0)

        # [53s - 60s] Telemetry Drawer & Presenter Mode Toggle
        update_subtitle(page, "GenAI Register: Google Gemini + Zero-Crash Fallback | 98% Test Coverage")
        btn_tele = page.locator("#btn-telemetry, button:has-text('Agent Telemetry')").first
        if btn_tele.is_visible():
            btn_tele.click()
            time.sleep(2.5)

        btn_pres = page.locator("#btn-presenter, button:has-text('Presenter Mode')").first
        if btn_pres.is_visible():
            btn_pres.click()
            time.sleep(2.5)

        time.sleep(2.0)

        # Finalize and close context to flush video
        print("💾 Closing browser to flush recorded video stream...")
        page.close()
        context.close()
        browser.close()

    # Find the generated video
    video_files = list(OUTPUT_DIR.glob("*.webm"))
    if not video_files:
        raise RuntimeError("No .webm video file found in output directory!")

    # Sort by creation time to get the latest
    latest_video = sorted(video_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]
    final_webm_path = OUTPUT_DIR / "saathi_copilot_demo.webm"

    if latest_video != final_webm_path:
        if final_webm_path.exists():
            final_webm_path.unlink()
        latest_video.rename(final_webm_path)

    file_size_mb = final_webm_path.stat().st_size / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"✅ DEMO VIDEO GENERATED SUCCESSFULLY!")
    print(f"📁 Path: {final_webm_path.resolve()}")
    print(f"📊 Size: {file_size_mb:.2f} MB")
    print(f"=======================================================\n")

    # Optional: Convert to MP4 if ffmpeg is available in PATH or playwright directory
    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        playwright_dir = Path(os.path.expanduser("~")) / "AppData" / "Local" / "ms-playwright"
        for candidate in playwright_dir.glob("**/ffmpeg*.exe"):
            if candidate.is_file():
                ffmpeg_bin = str(candidate)
                break

    if ffmpeg_bin:
        final_mp4_path = OUTPUT_DIR / "saathi_copilot_demo.mp4"
        print(f"🎞️ Converting WebM to MP4 via {ffmpeg_bin}...")
        try:
            subprocess.run(
                [
                    ffmpeg_bin,
                    "-y",
                    "-i",
                    str(final_webm_path),
                    "-c:v",
                    "libx264",
                    "-preset",
                    "fast",
                    "-crf",
                    "22",
                    "-c:a",
                    "aac",
                    str(final_mp4_path),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"✅ MP4 Version: {final_mp4_path.resolve()} ({final_mp4_path.stat().st_size / (1024*1024):.2f} MB)")
        except Exception as e:
            print(f"⚠️ Could not convert to MP4: {e}")

    return str(final_webm_path.resolve())


if __name__ == "__main__":
    try:
        run_demo_recording()
    except Exception as exc:
        print(f"❌ Error during video recording: {exc}", file=sys.stderr)
        sys.exit(1)
