"""Layered guardrail module enforcing policy-as-code, canary leak detection, and civic domain locking.

Implements Layer 1 (Deterministic Input Shield), Civic PII Masking,
Domain Scope Enforcement, and Layer 3 (Output Canary Validation).
"""

import re
import unicodedata
from typing import List, Pattern, Tuple

# Mandatory system canary token for prompt leak detection
CANARY_TOKEN: str = "PW-CANARY-7f3a91"

INJECTION_PATTERNS: List[str] = [
    r"ignore\s+(?:previous|all|prior|above)\s+instructions",
    r"disregard\s+.*(?:instructions|directions|guidelines|rules)",
    r"system\s+prompt",
    r"developer\s+mode",
    r"dan\s+mode",
    r"reveal\s+.*(?:prompt|instructions|configuration|canary|secret)",
    r"repeat\s+everything\s+(?:above|from the start)",
    r"leak\s+.*(?:prompt|canary|system|token)",
    r"bypass\s+.*(?:guardrail|filter|security|safety)",
    r"you\s+are\s+now\s+(?:unfiltered|jailbroken|godmode|unrestricted)",
    r"act\s+as\s+(?:an?\s+unrestricted|a\s+hacker|dan)",
    r"override\s+.*(?:safety|policy|instructions)",
]

OUT_OF_DOMAIN_PATTERNS: List[str] = [
    r"\b(?:crypto|bitcoin|ethereum|forex|stock\s+tips|day\s+trading|gambling|casino|betting)\b",
    r"\b(?:poem|poetry|song\s+lyrics|fiction\s+story|dating\s+advice|horoscope|astrology)\b",
    r"\b(?:cheat\s+codes|video\s+game\s+hacks)\b",
]

# Civic PII patterns to mask per domain-packs/civic.md
AADHAAR_PATTERN: Pattern[str] = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
PHONE_PATTERN: Pattern[str] = re.compile(r"(?:\+91[-\s]?|\b)[6-9]\d{9}\b")
PAN_PATTERN: Pattern[str] = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b", re.IGNORECASE)
BANK_ACC_PATTERN: Pattern[str] = re.compile(r"\b\d{11,18}\b")

COMPILED_INJECTIONS: List[Pattern[str]] = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]
COMPILED_OUT_OF_DOMAIN: List[Pattern[str]] = [re.compile(p, re.IGNORECASE) for p in OUT_OF_DOMAIN_PATTERNS]
HTML_TAG_PATTERN: Pattern[str] = re.compile(r"<[^>]+>")


def normalize_text(text: str) -> str:
    """Normalize untrusted text: Unicode NFKC, strip zero-width chars, HTML, collapse whitespace.

    Args:
        text: Raw input string to sanitize.

    Returns:
        str: Cleaned, normalized unicode string.

    Raises:
        None
    """
    if not text:
        return ""
    # Unicode NFKC normalization
    normalized: str = unicodedata.normalize("NFKC", text)
    # Strip zero-width characters (ZWSP, ZWNJ, ZWJ, BOM, etc.)
    normalized = re.sub(r"[\u200B-\u200D\uFEFF]", "", normalized)
    # Strip HTML tags
    normalized = HTML_TAG_PATTERN.sub(" ", normalized)
    # Collapse whitespace
    normalized = " ".join(normalized.split())
    return normalized


def mask_civic_pii(text: str) -> str:
    """Mask citizen sensitive identifiers: Aadhaar, Indian mobile numbers, PAN, Bank accounts.

    Args:
        text: Normalized text potentially containing PII.

    Returns:
        str: Text with sensitive citizen numbers safely redacted.

    Raises:
        None
    """
    if not text:
        return ""
    masked: str = AADHAAR_PATTERN.sub("XXXX-XXXX-XXXX", text)
    masked = PHONE_PATTERN.sub("+91-XXXXX-XXXXX", masked)
    masked = PAN_PATTERN.sub("[MASKED_PAN]", masked)
    masked = BANK_ACC_PATTERN.sub("[MASKED_BANK_ACC]", masked)
    return masked


def validate_input_l1(text: str) -> Tuple[bool, str, str]:
    """Layer 1 Deterministic Input Shield.

    1. Clamp length to 5,000 characters.
    2. Normalize Unicode NFKC, strip HTML, collapse spaces.
    3. Detect prompt injection, multi-attack vectors, and jailbreak patterns.
    4. Redact citizen PII (Aadhaar, PAN, phone).

    Args:
        text: Untrusted raw user input.

    Returns:
        Tuple[bool, str, str]: (is_valid, decision_reason, sanitized_text).

    Raises:
        None
    """
    if text is None:
        return False, "Input cannot be null", ""

    if len(text) > 5000:
        return False, "Input exceeds 5,000 character limit", text[:5000]

    normalized: str = normalize_text(text)
    lowered: str = normalized.lower()

    # Injection pattern matching (covers single and multi-vector combinations)
    for pattern in COMPILED_INJECTIONS:
        if pattern.search(lowered):
            return False, f"Prompt injection pattern detected: '{pattern.pattern}'", normalized

    # Mask any citizen PII in clean normalized text
    sanitized: str = mask_civic_pii(normalized)
    return True, "PASS", sanitized


def check_domain_scope(text: str) -> Tuple[bool, str]:
    """Verify input falls strictly within gig worker, welfare, and civic support scope.

    Args:
        text: Sanitized user query text.

    Returns:
        Tuple[bool, str]: (is_in_scope, explanation).

    Raises:
        None
    """
    lowered: str = text.lower()
    for pattern in COMPILED_OUT_OF_DOMAIN:
        if pattern.search(lowered):
            return False, f"Request matches out-of-scope domain pattern: '{pattern.pattern}'"
    return True, "IN_SCOPE"


def validate_output_l3(output_text: str) -> Tuple[bool, str]:
    """Layer 3 Output Validation: checks canary token leaks and structural safety.

    Args:
        output_text: Raw LLM or tool generated output.

    Returns:
        Tuple[bool, str]: (is_safe, failure_reason).

    Raises:
        None
    """
    if not output_text:
        return True, "PASS"
    if CANARY_TOKEN in output_text:
        return False, "CANARY_LEAK"
    return True, "PASS"
