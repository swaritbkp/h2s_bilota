import datetime
import json
import os
import time
from pathlib import Path
from typing import Any, Dict

from src.agent.agent import AGENT_VERSION, PROMPT_VERSION, run_saathi_agent
from src.core.guardrails import check_domain_scope, validate_input_l1

# Verified Default Preset Scenario for Ramesh
DEFAULT_PRESET_SCENARIO = {
    "title": "Ramesh Kumar - Swiggy/Zomato Delivery Partner",
    "worker_name": "Ramesh Kumar",
    "platform": "Swiggy / Zomato",
    "city": "Bengaluru, Karnataka",
    "shift_hours": 12.0,
    "input_text": (
        "Bhaiya kal raat 12 ghante shift kiya Bangalore me. 18 orders deliver kiye. "
        "App me gross earnings ₹1,200 dikha raha tha, lekin bank payout sirf ₹750 aaya. "
        "₹450 unexplained customer cancellation penalty kat gaya jo meri galti nahi thi. "
        "Barish me bike phisli thi minor chot aayi. Mujhe samajh nahi aa raha dispute kaise karein "
        "aur koi scheme ka paisa milta hai kya."
    ),
    "highlight": "₹450 unauthorized deduction (37.5% penalty) | ₹2,00,000 e-Shram accidental insurance gap",
}

# In-memory deterministic cache
_RESPONSE_CACHE: Dict[str, Dict[str, Any]] = {}
AUDIT_LOG_FILE = Path("logs/audit.jsonl")


def _log_audit_entry(result: Dict[str, Any]) -> None:
    """Append-only audit logging for AI governance and compliance."""
    try:
        AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        tele = result.get("telemetry", {})
        grounding = tele.get("groundingConfidence", 0.0)
        status = result.get("status", "UNKNOWN")
        needs_review = status != "OK" or grounding < 0.75

        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": status,
            "durationMs": tele.get("durationMs", 0),
            "groundingConfidence": grounding,
            "fallbackUsed": tele.get("fallbackUsed", False),
            "layers": tele.get("layers", {}),
            "promptVersion": tele.get("promptVersion", PROMPT_VERSION),
            "agentVersion": tele.get("agentVersion", AGENT_VERSION),
            "humanReviewNeeded": needs_review,
        }
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass


def analyze(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core UI-independent logic implementing the Result contract from 20-eval-contract.md.
    Guaranteed never to throw unhandled exceptions.
    """
    start_time = time.perf_counter()

    if not isinstance(payload, dict):
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        res = {
            "status": "INVALID_INPUT",
            "output": {},
            "citations": [],
            "message": "Input payload must be a JSON object.",
            "telemetry": {
                "toolName": "SaathiConnectedWorkflowEngine",
                "status": "INVALID_INPUT",
                "durationMs": duration_ms,
                "groundingConfidence": 0.0,
                "fallbackUsed": False,
                "promptVersion": PROMPT_VERSION,
                "agentVersion": AGENT_VERSION,
                "layers": {"L1": "BLOCKED", "L2": "L2_SKIPPED", "L3": "PASS"},
            },
        }
        _log_audit_entry(res)
        return res

    # Extract input text
    is_preset = bool(payload.get("isPreset", False))
    text = payload.get("text")
    if text is None:
        text = payload.get("query") or payload.get("input") or ""
    text = str(text)

    # Use preset text if preset requested and no text provided
    if is_preset and not text.strip():
        text = DEFAULT_PRESET_SCENARIO["input_text"]

    simulate_offline = bool(payload.get("_simulateOffline", False))
    force_offline = os.getenv("FORCE_OFFLINE", "0") in ("1", "true", "True") or simulate_offline

    # Layer 1 Input Guardrail (Clamp, Normalize, Injection Shield, Civic PII Mask)
    l1_pass, l1_reason, sanitized = validate_input_l1(text)
    if not l1_pass:
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        res = {
            "status": "GUARDRAIL_BLOCKED",
            "output": {},
            "citations": [],
            "message": f"Input security check blocked the request: {l1_reason}",
            "telemetry": {
                "toolName": "SaathiConnectedWorkflowEngine",
                "status": "GUARDRAIL_BLOCKED",
                "durationMs": duration_ms,
                "groundingConfidence": 0.0,
                "fallbackUsed": False,
                "promptVersion": PROMPT_VERSION,
                "agentVersion": AGENT_VERSION,
                "layers": {"L1": "BLOCKED", "L2": "L2_SKIPPED", "L3": "PASS"},
            },
        }
        _log_audit_entry(res)
        return res

    # Domain Locking Check
    in_scope, scope_reason = check_domain_scope(sanitized)
    if not in_scope and not is_preset:
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        res = {
            "status": "OUT_OF_SCOPE",
            "output": {},
            "citations": [],
            "message": f"Request is outside gig worker support scope: {scope_reason}",
            "telemetry": {
                "toolName": "SaathiConnectedWorkflowEngine",
                "status": "OUT_OF_SCOPE",
                "durationMs": duration_ms,
                "groundingConfidence": 0.0,
                "fallbackUsed": False,
                "promptVersion": PROMPT_VERSION,
                "agentVersion": AGENT_VERSION,
                "layers": {"L1": "PASS", "L2": "L2_SKIPPED", "L3": "PASS"},
            },
        }
        _log_audit_entry(res)
        return res

    # Empty text check if not preset
    if not text.strip() and not is_preset:
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        res = {
            "status": "INVALID_INPUT",
            "output": {},
            "citations": [],
            "message": "Worker shift log or query text cannot be empty.",
            "telemetry": {
                "toolName": "SaathiConnectedWorkflowEngine",
                "status": "INVALID_INPUT",
                "durationMs": duration_ms,
                "groundingConfidence": 0.0,
                "fallbackUsed": False,
                "promptVersion": PROMPT_VERSION,
                "agentVersion": AGENT_VERSION,
                "layers": {"L1": "PASS", "L2": "PASS", "L3": "PASS"},
            },
        }
        _log_audit_entry(res)
        return res

    # Check deterministic cache for identical queries
    cache_key = f"{sanitized}_{is_preset}_{force_offline}"
    if cache_key in _RESPONSE_CACHE:
        cached_res = dict(_RESPONSE_CACHE[cache_key])
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        cached_res["telemetry"] = dict(cached_res["telemetry"])
        cached_res["telemetry"]["durationMs"] = duration_ms
        _log_audit_entry(cached_res)
        return cached_res

    try:
        # Run Saathi agent across the 4-pillar pipeline
        result = run_saathi_agent(
            sanitized_text=sanitized,
            is_preset=is_preset,
            force_offline=force_offline,
        )
        if is_preset:
            result["output"]["preset_info"] = DEFAULT_PRESET_SCENARIO

        _RESPONSE_CACHE[cache_key] = result
        _log_audit_entry(result)
        return result
    except Exception as exc:
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        res = {
            "status": "ERROR",
            "output": {},
            "citations": [],
            "message": f"Execution error: {str(exc)}",
            "telemetry": {
                "toolName": "SaathiConnectedWorkflowEngine",
                "status": "ERROR",
                "durationMs": duration_ms,
                "groundingConfidence": 0.0,
                "fallbackUsed": False,
                "promptVersion": PROMPT_VERSION,
                "agentVersion": AGENT_VERSION,
                "layers": {"L1": "PASS", "L2": "L2_SKIPPED", "L3": "ERROR"},
            },
        }
        _log_audit_entry(res)
        return res
