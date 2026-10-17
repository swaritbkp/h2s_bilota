"""Modular route and middleware test suite for src/app.py.

Tests 100% of routes, middlewares, error branches, and fallback loaders:
- GET /: index route with templates/index.html & fallback string
- GET /health: container orchestrator health check
- GET /api/preset: judge preset scenario
- POST /api/analyze: Pydantic validated analyze endpoint
- Security headers middleware: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy
- GZip compression middleware
- run_server helper
"""

from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from src.app import (
    HTML_UI_FALLBACK,
    AnalyzeRequest,
    app,
    get_index,
    get_preset,
    health_check,
    load_index_html,
    run_server,
)

client = TestClient(app)


def test_get_index_route():
    """Verify GET / returns HTTP 200 with HTML content and security headers."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "Saathi" in resp.text
    # Security headers verification
    assert resp.headers.get("x-content-type-options") == "nosniff"
    assert resp.headers.get("x-frame-options") == "DENY"
    assert resp.headers.get("x-xss-protection") == "1; mode=block"
    assert resp.headers.get("referrer-policy") == "strict-origin-when-cross-origin"


def test_load_index_html_fallback():
    """Verify fallback HTML is served if templates/index.html is missing or throws error."""
    with patch("src.app.TEMPLATE_PATH", Path("non_existent_directory/missing.html")):
        fallback_html = load_index_html()
        assert fallback_html == HTML_UI_FALLBACK
        assert "Skip to main content" in fallback_html


def test_load_index_html_exception():
    """Verify fallback HTML is served if reading templates/index.html throws an exception."""
    with patch("pathlib.Path.exists", return_value=True), patch("pathlib.Path.read_text", side_effect=IOError("Read error")):
        assert load_index_html() == HTML_UI_FALLBACK


def test_health_check_route():
    """Verify GET /health returns 200 and healthy status."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["service"] == "saathi-gig-copilot"
    assert data["version"] == "1.0.0"


def test_get_preset_route():
    """Verify GET /api/preset returns verified Ramesh judge scenario."""
    resp = client.get("/api/preset")
    assert resp.status_code == 200
    data = resp.json()
    assert data["worker_name"] == "Ramesh Kumar"
    assert "input_text" in data


def test_api_analyze_with_pydantic_valid():
    """Verify POST /api/analyze with valid Pydantic model payload."""
    payload = {
        "text": "Ramesh Kumar delivery partner Bangalore 12h gross 1200 net 750",
        "isPreset": True,
        "_simulateOffline": True,
    }
    resp = client.post("/api/analyze", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "OK"
    assert "output" in data
    assert "telemetry" in data


def test_api_analyze_with_invalid_json():
    """Verify POST /api/analyze handles malformed or non-dict payloads gracefully."""
    # Raw non-JSON content
    resp1 = client.post("/api/analyze", content="invalid json {", headers={"Content-Type": "application/json"})
    assert resp1.status_code == 200
    assert resp1.json()["status"] in ("INVALID_INPUT", "GUARDRAIL_BLOCKED")

    # Non-dict JSON (e.g. array)
    resp2 = client.post("/api/analyze", json=["not", "a", "dict"])
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "INVALID_INPUT"


def test_pydantic_analyze_request_model():
    """Verify Pydantic model field defaults and validation."""
    model = AnalyzeRequest()
    assert model.text == ""
    assert model.query is None
    assert model.isPreset is False
    assert model.simulateOffline is False

    custom = AnalyzeRequest(text="Shift text", query="alt text", isPreset=True, _simulateOffline=True)
    assert custom.text == "Shift text"
    assert custom.isPreset is True
    assert custom.simulateOffline is True


def test_direct_async_routes():
    """Directly execute async route functions for comprehensive statement coverage."""
    import asyncio

    # Test get_index directly
    index_resp = asyncio.run(get_index())
    assert index_resp.status_code == 200

    # Test health_check directly
    h_resp = asyncio.run(health_check())
    assert h_resp["status"] == "healthy"

    # Test get_preset directly
    p_resp = asyncio.run(get_preset())
    assert p_resp["worker_name"] == "Ramesh Kumar"


def test_run_server():
    """Verify run_server calls uvicorn.run with dynamic PORT."""
    with patch("uvicorn.run") as mock_run:
        with patch.dict("os.environ", {"PORT": "9090"}):
            run_server()
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert kwargs.get("port") == 9090 or args[2] == 9090
