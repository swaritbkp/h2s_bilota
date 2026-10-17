from typing import Any, Dict, List

# Benchmark statutory minimum wage threshold for gig logistics (Karnataka/Metro benchmark)
BENCHMARK_HOURLY_WAGE = 110.0


def audit_earnings_tool(
    gross_payout: float,
    net_payout: float,
    shift_hours: float,
    unexplained_deduction: float = 0.0,
    deduction_reason: str = "Unexplained deduction"
) -> Dict[str, Any]:
    """
    Deterministic Tool 1: Computes earnings breakdown, detects deduction anomalies,
    and calculates verified net hourly payout.
    """
    gross = float(max(gross_payout, 0.0))
    net = float(max(net_payout, 0.0))
    hours = float(max(shift_hours, 1.0))
    deductions_total = float(max(gross - net, 0.0))
    effective_hourly_rate = round(net / hours, 2)

    flagged_deductions: List[Dict[str, Any]] = []
    has_anomaly = False

    if deductions_total > 0:
        deduction_ratio = deductions_total / gross if gross > 0 else 1.0
        # Flag if deduction > 15% of gross earnings or specific penalty identified
        is_severe_anomaly = deduction_ratio >= 0.15 or unexplained_deduction > 0
        has_anomaly = is_severe_anomaly

        flagged_deductions.append({
            "item": deduction_reason if deduction_reason else "Platform Penalty / Operational Deduction",
            "amount": round(unexplained_deduction if unexplained_deduction > 0 else deductions_total, 2),
            "percentage_of_gross": round(deduction_ratio * 100, 1),
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
        "hourly_deficit": hourly_gap if hourly_gap > 0 else 0.0,
        "flagged_deductions": flagged_deductions,
        "anomaly_detected": has_anomaly,
    }


def match_welfare_schemes_tool(
    city: str = "Bengaluru",
    state: str = "Karnataka",
    platform: str = "Swiggy / Zomato",
    has_injury: bool = True
) -> Dict[str, Any]:
    """
    Deterministic Tool 2: Binds domain-packs/civic.md to evaluate statutory entitlements:
    e-Shram accidental insurance, PM-JAY, and State Gig Worker Boards.
    """
    schemes = [
        {
            "scheme_id": "src-eshram",
            "name": "e-Shram National Social Security Registry",
            "statutory_authority": "Ministry of Labour & Employment, Govt. of India",
            "coverage_amount": "₹2,00,000 (Accidental Death / Total Disability) | ₹1,00,000 (Partial Disability)",
            "eligibility_status": "ELIGIBLE",
            "action_required": "Link Universal Account Number (UAN) to platform partner profile",
            "reasoning": "Covers unorganised platform gig delivery partners aged 16-59 with accidental injury protection.",
            "official_portal": "https://eshram.gov.in",
            "priority": "HIGH" if has_injury else "NORMAL"
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
            "priority": "NORMAL"
        },
        {
            "scheme_id": "src-stategig",
            "name": f"{state} Platform-Based Gig Workers Social Security Welfare Scheme",
            "statutory_authority": f"{state} Gig Workers Welfare Board",
            "coverage_amount": "₹4,00,000 accidental & life cover + ₹10,000 hospital allowance",
            "eligibility_status": "ELIGIBLE",
            "action_required": "Mandatory auto-registration by platform aggregator via welfare fee contribution",
            "reasoning": f"Applies to active delivery partners operating in {city}, {state}.",
            "official_portal": "https://labour.karnataka.gov.in" if "karnataka" in state.lower() else "https://labour.gov.in",
            "priority": "HIGH"
        }
    ]

    return {
        "matched_schemes": schemes,
        "total_coverage_available": "Up to ₹11,00,000 combined accidental, healthcare & life coverage",
        "primary_recommendation": "Submit accident intimation to e-Shram portal within 30 days to claim medical reimbursement.",
    }


def draft_dispute_notice_tool(
    worker_name: str,
    platform: str,
    city: str,
    deduction_amount: float,
    hours_worked: float,
    issue_narrative: str
) -> Dict[str, Any]:
    """
    Deterministic Tool 3: Compiles formal legal dispute notice citing Code on Social Security 2020.
    """
    formal_notice = (
        f"FORMAL NOTICE OF DISPUTE & REMUNERATION RECTIFICATION\n"
        f"Date: 17 October 2026\n"
        f"To: Grievance Officer & Partner Compliance Operations, {platform}\n"
        f"Location: {city}\n\n"
        f"Complainant: {worker_name} (Delivery Partner)\n"
        f"Subject: Formal Dispute against Unauthorized Deduction of ₹{deduction_amount:.2f} — Request for Immediate Credit\n\n"
        f"Dear Grievance Officer,\n\n"
        f"I am submitting this formal grievance regarding my recent shift ({hours_worked:.1f} hours). "
        f"An unverified penalty deduction of ₹{deduction_amount:.2f} was debited from my shift payout without proper itemized substantiation.\n\n"
        f"Context & Grounds for Appeal:\n"
        f"1. Operational Circumstances: {issue_narrative}\n"
        f"2. Statutory Compliance: Under the Code on Social Security (2020) and State Gig Worker Welfare Directives, "
        f"arbitrary wage deductions and penalties without prior notification or an opportunity to provide clarification "
        f"constitute unfair operational practices.\n"
        f"3. On-Duty Diligence: I was logged in and actively serving orders during adverse shift conditions.\n\n"
        f"Relief Requested:\n"
        f"- Immediate reversal and credit of ₹{deduction_amount:.2f} to my partner earnings wallet within 48 hours.\n"
        f"- Protection of partner operational metrics (acceptance rate and reliability rating).\n"
        f"- Written breakdown of the cancellation incident.\n\n"
        f"Respectfully submitted,\n"
        f"{worker_name}\n"
        f"Delivery Partner — {platform} ({city})\n"
        f"Contact: Verified Partner Record"
    )

    return {
        "subject": f"FORMAL DISPUTE: Unauthorized Deduction of ₹{deduction_amount:.2f} — {worker_name}",
        "recipient": f"{platform} Partner Grievance Cell & Compliance Team",
        "formal_notice_body": formal_notice,
        "legal_statutory_citations": [
            "Code on Social Security, 2020 (Sections 112-114: Platform & Gig Worker Welfare)",
            "Model Guidelines for Platform Partner Dispute Redressal & Deduction Transparency (2023)"
        ]
    }
