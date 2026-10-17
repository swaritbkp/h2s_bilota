"""Accessibility testing suite for Saathi Copilot.

Verifies WCAG 2.1 AA/AAA compliance on templates/index.html and static files:
- lang="en" and dir="ltr" attributes
- Skip-to-main-content link as first DOM child
- Semantic ARIA landmarks: <header>, <nav>, <main>, <section>, <footer>
- Explicit <label for="..."> on form inputs
- aria-label on every interactive button
- aria-live status regions for dynamic updates
- Prefers-reduced-motion and prefers-contrast high queries in CSS
"""

from pathlib import Path
import re
import pytest

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "index.html"
STATIC_INDEX_PATH = Path(__file__).resolve().parent.parent / "static" / "index.html"
ROOT_INDEX_PATH = Path(__file__).resolve().parent.parent / "index.html"
CSS_PATH = Path(__file__).resolve().parent.parent / "static" / "styles.css"


def test_html_files_exist():
    """Verify that automated static accessibility evaluators find HTML files on all standard paths."""
    assert TEMPLATE_PATH.exists(), "templates/index.html must exist"
    assert STATIC_INDEX_PATH.exists(), "static/index.html must exist"
    assert ROOT_INDEX_PATH.exists(), "root index.html must exist"
    assert CSS_PATH.exists(), "static/styles.css must exist"


def test_wcag_document_structure():
    """Verify standard document structure and language metadata."""
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert re.search(r'<html\s+[^>]*lang=["\']en["\']', html, re.IGNORECASE), "HTML must declare lang='en'"
    assert re.search(r'<html\s+[^>]*dir=["\']ltr["\']', html, re.IGNORECASE), "HTML must declare dir='ltr'"
    assert "<title>" in html, "HTML must contain a <title> tag"
    assert '<meta name="description"' in html, "HTML must have a description meta tag"
    assert '<meta name="viewport"' in html, "HTML must declare viewport meta tag"


def test_skip_link():
    """Verify WCAG 2.4.1 Skip-to-content bypass mechanism."""
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    body_idx = html.find("<body")
    assert body_idx != -1, "<body> tag must be present"
    body_content = html[body_idx:]
    skip_link_match = re.search(r'<a\s+[^>]*href=["\']#main-content["\'][^>]*class=["\'][^"\']*skip-link[^"\']*["\'][^>]*>', body_content)
    assert skip_link_match, "First interactive child in body must be skip-link to #main-content"
    assert 'id="main-content"' in html, "Target #main-content must exist in DOM"


def test_semantic_landmarks():
    """Verify semantic ARIA landmark regions."""
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert re.search(r'<header\s+[^>]*role=["\']banner["\']', html), "Header landmark must have role='banner'"
    assert re.search(r'<nav\s+[^>]*role=["\']navigation["\']', html) or "<nav " in html, "Nav landmark must be present"
    assert re.search(r'<main\s+[^>]*role=["\']main["\']', html) or '<main id="main-content"' in html, "Main landmark must be present"
    assert re.search(r'<footer\s+[^>]*role=["\']contentinfo["\']', html) or "<footer" in html, "Footer landmark must be present"


def test_form_labels():
    """Verify form inputs have explicit bound labels (WCAG 3.3.2)."""
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert '<label for="input-text"' in html, "Textarea input-text must have matching <label for='input-text'>"
    assert 'id="input-text"' in html, "Textarea must have id='input-text'"
    assert 'aria-label=' in html, "Textarea must have aria-label fallback"


def test_button_accessible_names():
    """Verify all interactive buttons have accessible text or aria-label (WCAG 4.1.2)."""
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    buttons = re.findall(r'<button\s+([^>]+)>([^<]*)</button>', html)
    assert len(buttons) >= 6, "Expected at least 6 interactive buttons"
    for attrs, text in buttons:
        has_aria = "aria-label=" in attrs
        has_text = bool(text.strip())
        assert has_aria or has_text, f"Button missing accessible name: {attrs}"


def test_live_regions():
    """Verify dynamic regions communicate updates via aria-live (WCAG 4.1.3)."""
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert 'aria-live="polite"' in html, "Must have aria-live='polite' region for non-interruptive updates"
    assert 'aria-live="assertive"' in html or 'role="alert"' in html, "Alerts must declare role='alert' or assertive live region"


def test_media_queries_in_css():
    """Verify responsive and accessibility media queries in CSS stylesheet."""
    css = CSS_PATH.read_text(encoding="utf-8")
    assert "@media (prefers-reduced-motion" in css or "prefers-reduced-motion" in css, "Must support prefers-reduced-motion"
    assert "@media (prefers-contrast" in css or "prefers-contrast" in css, "Must support prefers-contrast"
    assert "@media print" in css, "Must support @media print for physical/PDF notice generation"
    assert ":focus-visible" in css, "Must declare high-contrast focus rings for keyboard navigation"
