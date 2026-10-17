#!/usr/bin/env python3
# eval/run_eval.py - measured eval harness (Python standard library only).
#
# Calls the app through its adapter, validates the Result contract
# (.agent/rules/20-eval-contract.md) and writes REAL measured results.
#
#   python eval/run_eval.py --mode http --target http://localhost:8000/api/analyze
#   python eval/run_eval.py --mode cmd  --target "python -m app.cli"
#
# Outputs: eval/benchmark-report.md, eval/results.json, eval/history/results-<timestamp>.json
# Exit code: 0 all executed cases passed, 1 some failed, 2 nothing executed.
import argparse
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

VALID_STATUS = {"OK", "GUARDRAIL_BLOCKED", "OUT_OF_SCOPE", "INVALID_INPUT", "ERROR"}
REQUIRED_TELEMETRY = ["toolName", "status", "durationMs", "fallbackUsed", "promptVersion"]


def call_http(url, payload, timeout):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def call_cmd(cmd, payload, timeout):
    proc = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True, shell=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "command exited with a non-zero code")
    return json.loads(proc.stdout)


def build_payload(case):
    payload = dict(case.get("input", {}))
    pad = case.get("padChars")
    if pad:
        payload["text"] = str(payload.get("text") or "") + ("A" * int(pad))
    if case.get("simulateOffline"):
        payload["_simulateOffline"] = True
    return payload


def evaluate(case, res, wall_ms):
    # Returns (problems, schema_ok, status, grounding, fallback_used)
    exp = case.get("expect", {})
    problems = []
    if not isinstance(res, dict):
        return ["response is not a JSON object"], False, None, None, False

    status = res.get("status")
    tel = res.get("telemetry") or {}
    missing = [k for k in REQUIRED_TELEMETRY if k not in tel]
    schema_ok = (status in VALID_STATUS) and not missing
    if status not in VALID_STATUS:
        problems.append("invalid status: %r" % (status,))
    if missing:
        problems.append("telemetry missing: " + ", ".join(missing))

    allowed = exp.get("status", ["OK"])
    if isinstance(allowed, str):
        allowed = [allowed]
    if status not in allowed:
        problems.append("status %s not in %s" % (status, allowed))

    if status == "OK":
        out = res.get("output")
        for key in exp.get("requiredKeys", []):
            if not isinstance(out, dict) or key not in out:
                problems.append("output missing key '%s'" % key)
        if exp.get("requireCitations") and not res.get("citations"):
            problems.append("no citations on an OK response")

    grounding = tel.get("groundingConfidence")
    if "minGrounding" in exp:
        if not isinstance(grounding, (int, float)) or grounding < exp["minGrounding"]:
            problems.append("grounding %r below %s" % (grounding, exp["minGrounding"]))

    max_ms = exp.get("maxLatencyMs", 5000)
    if wall_ms > max_ms:
        problems.append("latency %d ms above budget %d ms" % (wall_ms, max_ms))

    blob = json.dumps(res, ensure_ascii=False).lower()
    for bad in exp.get("mustNotContain", []):
        if bad.lower() in blob:
            problems.append("response contains forbidden text '%s'" % bad)

    fallback_used = bool(tel.get("fallbackUsed"))
    if "fallbackUsed" in exp and fallback_used != bool(exp["fallbackUsed"]):
        problems.append("fallbackUsed was %s, expected %s" % (fallback_used, exp["fallbackUsed"]))

    return problems, schema_ok, status, grounding, fallback_used


def main():
    ap = argparse.ArgumentParser(description="Measured eval harness")
    ap.add_argument("--mode", choices=["http", "cmd"], required=True)
    ap.add_argument("--target", required=True, help="URL (http) or shell command (cmd)")
    ap.add_argument("--suite", default="eval/test-suite.json")
    ap.add_argument("--report", default="eval/benchmark-report.md")
    ap.add_argument("--timeout", type=float, default=20.0)
    args = ap.parse_args()

    suite_path = Path(args.suite)
    if not suite_path.exists():
        print("Suite not found: %s (copy eval/test-suite.example.json first)" % suite_path)
        return 2
    suite = json.loads(suite_path.read_text(encoding="utf-8"))
    cases = suite["cases"] if isinstance(suite, dict) else suite

    rows = []
    for case in cases:
        cid = case.get("id", "case")
        if case.get("todo"):
            rows.append({"id": cid, "vector": case.get("vector", ""), "result": "SKIPPED", "detail": "todo case not filled in"})
            continue
        payload = build_payload(case)
        start = time.perf_counter()
        try:
            res = call_http(args.target, payload, args.timeout) if args.mode == "http" else call_cmd(args.target, payload, args.timeout)
            err = None
        except Exception as exc:
            res, err = None, str(exc)
        wall_ms = int((time.perf_counter() - start) * 1000)

        if err:
            rows.append({"id": cid, "vector": case.get("vector", ""), "result": "FAIL", "status": "NO_RESPONSE",
                         "latencyMs": wall_ms, "detail": "call failed: " + err})
            continue
        problems, schema_ok, status, grounding, fb = evaluate(case, res, wall_ms)
        rows.append({
            "id": cid, "vector": case.get("vector", ""), "result": "FAIL" if problems else "PASS",
            "status": status, "schema": schema_ok, "grounding": grounding, "latencyMs": wall_ms,
            "fallbackUsed": fb, "detail": "; ".join(problems),
        })

    ran = [r for r in rows if r["result"] in ("PASS", "FAIL")]
    passed = [r for r in ran if r["result"] == "PASS"]
    failed = [r for r in ran if r["result"] == "FAIL"]
    skipped = [r for r in rows if r["result"] == "SKIPPED"]
    lat = [r["latencyMs"] for r in ran if "latencyMs" in r]
    grd = [r["grounding"] for r in ran if isinstance(r.get("grounding"), (int, float))]
    pass_rate = (len(passed) / len(ran)) if ran else 0.0
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary = {
        "timestamp": stamp, "mode": args.mode, "target": args.target,
        "executed": len(ran), "passed": len(passed), "failed": len(failed), "skipped": len(skipped),
        "passRate": round(pass_rate, 4),
        "avgLatencyMs": round(sum(lat) / len(lat), 1) if lat else None,
        "maxLatencyMs": max(lat) if lat else None,
        "avgGrounding": round(sum(grd) / len(grd), 3) if grd else None,
    }

    lines = ["# Benchmark Report (MEASURED)", "",
             "Generated by `eval/run_eval.py` on %s. Do not edit by hand." % stamp, "",
             "| Metric | Value |", "|---|---|",
             "| Executed / Passed / Failed / Skipped | %d / %d / %d / %d |" % (len(ran), len(passed), len(failed), len(skipped)),
             "| Pass rate | %.1f%% |" % (pass_rate * 100),
             "| Avg latency (ms) | %s |" % summary["avgLatencyMs"],
             "| Max latency (ms) | %s |" % summary["maxLatencyMs"],
             "| Avg grounding (OK responses) | %s |" % summary["avgGrounding"], "",
             "| Case | Vector | Status | Schema | Grounding | Latency (ms) | Fallback | Result | Detail |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["id"], r.get("vector", ""), r.get("status", "-"),
            ("PASS" if r.get("schema") else "FAIL") if "schema" in r else "-",
            r.get("grounding", "-"), r.get("latencyMs", "-"),
            r.get("fallbackUsed", "-"), r["result"], r.get("detail", "") or ""))
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    results = {"summary": summary, "cases": rows}
    Path("eval/results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    hist = Path("eval/history")
    hist.mkdir(parents=True, exist_ok=True)
    (hist / ("results-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".json")).write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("Executed %d | Passed %d | Failed %d | Skipped %d | Pass rate %.1f%%" % (len(ran), len(passed), len(failed), len(skipped), pass_rate * 100))
    for r in failed:
        print("  FAIL %s: %s" % (r["id"], r["detail"]))
    if not ran:
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
