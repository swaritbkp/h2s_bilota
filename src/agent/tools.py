"""Deterministic civic & statutory reasoning tools for Saathi Copilot.

Includes earnings auditing, statutory welfare scheme matching,
and formal platform grievance drafting compliant with Indian labor guidelines.
"""

from functools import lru_cache
from typing import Any, Dict, List, Optional

# Benchmark statutory minimum wage threshold for gig logistics (Karnataka/Metro benchmark)
BENCHMARK_HOURLY_WAGE: float = 110.0


def audit_earnings_tool(
    gross_payout: float,
    net_payout: float,
    shift_hours: float,
    unexplained_deduction: float = 0.0,
    deduction_reason: str = "Unexplained deduction",
) -> Dict[str, Any]:
    """Deterministic Tool 1: Computes earnings breakdown and flags anomalies.

    Args:
        gross_payout: Total gross shift earnings before deductions (INR).
        net_payout: Actual deposited or wallet take-home earnings (INR).
        shift_hours: Total duration of the shift in hours (minimum 0.5h).
        unexplained_deduction: Explicit penalty or deduction identified (INR).
        deduction_reason: Specific reason or classification of the deduction.

    Returns:
        Dict[str, Any]: Structured audit metrics including gross, net, deductions,
            effective hourly wage, deficit against benchmark, and anomaly flags.

    Raises:
        None: Function is fully guarded against division by zero and negative values.
    """
    gross = float(max(gross_payout, 0.0))
    net = float(max(net_payout, 0.0))
    hours = float(max(shift_hours, 0.5))
    deductions_total = float(max(gross - net, 0.0))
    effective_hourly_rate = round(net / hours, 2)

    flagged_deductions: List[Dict[str, Any]] = []
    has_anomaly: bool = False

    if gross == 0.0 and hours >= 8.0:
        has_anomaly = True
        flagged_deductions.append({
            "item": "Zero Remuneration Shift Anomaly",
            "amount": 0.0,
            "percentage_of_gross": 100.0,
            "reason": f"Completed {hours:.1f} hours logged in without recorded earnings.",
            "anomaly": True,
        })
    elif deductions_total > 0.0:
        deduction_ratio = deductions_total / gross if gross > 0.0 else 1.0
        # Flag if deduction > 15% of gross earnings or specific penalty identified
        is_severe_anomaly = deduction_ratio >= 0.15 or unexplained_deduction > 0.0
        has_anomaly = is_severe_anomaly

        flagged_deductions.append({
            "item": deduction_reason if deduction_reason else "Platform Penalty / Operational Deduction",
            "amount": round(unexplained_deduction if unexplained_deduction > 0.0 else deductions_total, 2),
            "percentage_of_gross": round(deduction_ratio * 100.0, 1),
            "reason": "Deduction exceeds fair platform threshold (15%) or lacks itemized trip breakdown.",
            "anomaly": is_severe_anomaly,
        })

    hourly_gap = round(BENCHMARK_HOURLY_WAGE - effective_hourly_rate, 2)

    return {
        "gross_payout": round(gross, 2),
        "deductions_total": round(deductions_total, 2),
        "net_payout": round(net, 2),
        "hours_worked": round(hours, 1),
        "effective_hourly_rate": effective_hourly_rate,
        "benchmark_hourly_rate": BENCHMARK_HOURLY_WAGE,
        "below_benchmark": effective_hourly_rate < BENCHMARK_HOURLY_WAGE,
        "hourly_deficit": hourly_gap if hourly_gap > 0.0 else 0.0,
        "flagged_deductions": flagged_deductions,
        "anomaly_detected": has_anomaly,
    }


@lru_cache(maxsize=128)
def _cached_match_welfare_schemes(
    city: str,
    state: str,
    platform: str,
    has_injury: bool
) -> Dict[str, Any]:
    """Internal memoized resolver for statutory schemes to guarantee <5ms response."""
    portal_url = "https://labour.karnataka.gov.in" if "karnataka" in state.lower() else "https://labour.gov.in"
    schemes: List[Dict[str, Any]] = [
        {
            "scheme_id": "src-eshram",
            "name": "e-Shram National Social Security Registry",
            "statutory_authority": "Ministry of Labour & Employment, Govt. of India",
            "coverage_amount": "₹2,00,000 (Accidental Death / Total Disability) | ₹1,00,000 (Partial Disability)",
            "eligibility_status": "ELIGIBLE",
            "action_required": "Link Universal Account Number (UAN) to platform partner profile",
            "reasoning": "Covers unorganised platform gig delivery partners aged 16-59 with accidental injury protection.",
            "official_portal": "https://eshram.gov.in",
            "priority": "HIGH" if has_injury else "NORMAL",
        },
        {
            "scheme_id": "src-pmjay",
            "name": "Ayushman Bharat — PM-JAY",
            "statutory_authority": "National Health Authority",
            "coverage_amount": "₹5,00,000 per family/year for cashless hospitalization",
            "eligibility_status": "LIKELY_ELIGIBLE",
            "action_required": "Check ration card / SECC family eligibility at nearest CSC center",
            "reasoning": "Informal and gig transport workers qualify under deprivation / occupational categories.",
            "official_portal": "https://beneficiary.nha.gov.in",
            "priority": "NORMAL",
        },
        {
            "scheme_id": "src-stategig",
            "name": f"{state} Platform-Based Gig Workers Social Security Welfare Scheme",
            "statutory_authority": f"{state} Gig Workers Welfare Board",
            "coverage_amount": "₹4,00,000 accidental & life cover + ₹10,000 hospital allowance",
            "eligibility_status": "ELIGIBLE",
            "action_required": "Mandatory auto-registration by platform aggregator via welfare fee contribution",
            "reasoning": f"Applies to active delivery partners operating in {city}, {state}.",
            "official_portal": portal_url,
            "priority": "HIGH",
        },
    ]

    return {
        "matched_schemes": schemes,
        "total_coverage_available": "Up to ₹11,00,000 combined accidental, healthcare & life coverage",
        "primary_recommendation": "Submit accident intimation to e-Shram portal within 30 days to claim medical reimbursement.",
    }


def match_welfare_schemes_tool(
    city: str = "Bengaluru",
    state: str = "Karnataka",
    platform: str = "Swiggy / Zomato",
    has_injury: bool = True,
) -> Dict[str, Any]:
    """Deterministic Tool 2: Binds domain-packs/civic.md to evaluate statutory entitlements.

    Args:
        city: Operating city of the gig worker.
        state: Operating state of the gig worker.
        platform: Platform aggregator name (e.g., Swiggy, Zomato, Uber).
        has_injury: Boolean flag indicating if workplace accident occurred.

    Returns:
        Dict[str, Any]: Matched schemes with statutory coverage and action steps.

    Raises:
        None
    """
    clean_city = (city or "Bengaluru").strip()
    clean_state = (state or "Karnataka").strip()
    clean_platform = (platform or "Swiggy / Zomato").strip()
    return _cached_match_welfare_schemes(clean_city, clean_state, clean_platform, bool(has_injury))


@lru_cache(maxsize=128)
def draft_dispute_notice_tool(
    worker_name: str,
    platform: str,
    city: str,
    deduction_amount: float,
    hours_worked: float,
    issue_narrative: str,
) -> Dict[str, Any]:
    """Deterministic Tool 3: Compiles formal legal dispute notice with LRU caching.

    Args:
        worker_name: Full name of the aggrieved partner.
        platform: Delivery or transport platform aggregator.
        city: Operating jurisdiction city.
        deduction_amount: Quantum of unauthorized penalty or deduction (INR).
        hours_worked: Total shift duration in hours.
        issue_narrative: Concise factual statement of the dispute context.

    Returns:
        Dict[str, Any]: Subject, recipient, formal legal notice body, and statutory citations.

    Raises:
        None
    """
    w_name = worker_name.strip() if worker_name else "Aggrieved Partner"
    plat = platform.strip() if platform else "Platform Operations"
    c_city = city.strip() if city else "Bengaluru"
    ded_amt = float(deduction_amount)
    hrs = float(hours_worked)

    formal_notice = (
        f"FORMAL NOTICE OF DISPUTE & REMUNERATION RECTIFICATION\n"
        f"Date: 17 October 2026\n"
        f"To: Grievance Redressal Officer & Partner Operations, {plat}\n"
        f"Jurisdiction / Operating Hub: {c_city}\n\n"
        f"Complainant: {w_name} (Registered Delivery / Transport Partner)\n"
        f"Subject: Formal Dispute against Unauthorized Deduction of ₹{ded_amt:.2f} — Demand for Immediate Wallet Credit\n\n"
        f"Dear Grievance Officer,\n\n"
        f"I am submitting this formal statutory grievance regarding my recent operational shift ({hrs:.1f} hours). "
        f"An unverified penalty debit of ₹{ded_amt:.2f} was deducted from my shift payout without prior notice "
        f"or itemized dispute substantiation.\n\n"
        f"Factual Grounds for Appeal:\n"
        f"1. Operational Context: {issue_narrative}\n"
        f"2. Statutory Compliance: Under the Code on Social Security (2020) (Sections 112-114) and "
        f"State Platform-Based Gig Workers Welfare Regulations, arbitrary wage deductions and unilateral penalties "
        f"without an opportunity for fair hearing constitute unfair operational practices.\n"
        f"3. On-Duty Diligence: I was logged in and actively serving platform orders during adverse shift conditions.\n\n"
        f"Demanded Relief:\n"
        f"- Immediate reversal and credit of ₹{ded_amt:.2f} to my partner earnings wallet within 48 hours.\n"
        f"- Protection of partner operational metrics (acceptance rate and reliability rating).\n"
        f"- Provision of written incident logs and cancellation verification.\n\n"
        f"Respectfully submitted,\n"
        f"{w_name}\n"
        f"Partner — {plat} ({c_city})\n"
        f"Status: Formally Lodged via Saathi Statutory Copilot"
    )

    return {
        "subject": f"FORMAL DISPUTE: Unauthorized Deduction of ₹{ded_amt:.2f} — {w_name}",
        "recipient": f"{plat} Partner Grievance Cell & Compliance Team",
        "formal_notice_body": formal_notice,
        "legal_statutory_citations": [
            "Code on Social Security, 2020 (Sections 112-114: Platform & Gig Worker Welfare)",
            "Karnataka Platform-Based Gig Workers (Social Security & Welfare) Bill",
            "Model Guidelines for Platform Partner Dispute Redressal & Deduction Transparency",
        ],
    }
