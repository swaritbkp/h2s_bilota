import re
import unicodedata
from typing import Tuple

# Mandatory system canary token for leak detection
CANARY_TOKEN = "PW-CANARY-7f3a91"

INJECTION_PATTERNS = [
    r"ignore\s+(?:previous|all|prior)\s+instructions",
    r"disregard\s+.*(?:instructions|directions|guidelines)",
    r"system\s+prompt",
    r"developer\s+mode",
    r"dan\s+mode",
    r"reveal\s+.*(?:prompt|instructions|configuration|canary)",
    r"repeat\s+everything\s+above",
    r"leak\s+.*(?:prompt|canary|system)",
    r"bypass\s+.*(?:guardrail|filter|security)",
]

OUT_OF_DOMAIN_PATTERNS = [
    r"\b(?:crypto|bitcoin|ethereum|forex|stock\s+tips|day\s+trading|gambling|casino|betting)\b",
    r"\b(?:poem|poetry|song\s+lyrics|fiction\s+story|dating\s+advice|horoscope|astrology)\b",
    r"\b(?:cheat\s+codes|video\s+game\s+hacks)\b",
]

# Civic PII patterns to mask per domain-packs/civic.md
AADHAAR_PATTERN = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b")
PAN_PATTERN = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b", re.IGNORECASE)
BANK_ACC_PATTERN = re.compile(r"\b\d{11,18}\b")

COMPILED_INJECTIONS = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]
COMPILED_OUT_OF_DOMAIN = [re.compile(p, re.IGNORECASE) for p in OUT_OF_DOMAIN_PATTERNS]
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def normalize_text(text: str) -> str:
    """Normalize input: Unicode NFKC, strip zero-width chars, HTML, collapse whitespace."""
    if not text:
        return ""
    # Unicode NFKC normalization
    normalized = unicodedata.normalize("NFKC", text)
    # Strip zero-width characters (ZWSP, ZWNJ, ZWJ, BOM, etc.)
    normalized = re.sub(r"[\u200B-\u200D\uFEFF]", "", normalized)
    # Strip HTML tags
    normalized = HTML_TAG_PATTERN.sub(" ", normalized)
    # Collapse whitespace
    normalized = " ".join(normalized.split())
    return normalized


def mask_civic_pii(text: str) -> str:
    """Mask citizen PII: Aadhaar, Indian mobile numbers, PAN, Bank accounts."""
    if not text:
        return ""
    masked = AADHAAR_PATTERN.sub("XXXX-XXXX-XXXX", text)
    masked = PHONE_PATTERN.sub("+91-XXXXX-XXXXX", masked)
    masked = PAN_PATTERN.sub("[MASKED_PAN]", masked)
    masked = BANK_ACC_PATTERN.sub("[MASKED_BANK_ACC]", masked)
    return masked


def validate_input_l1(text: str) -> Tuple[bool, str, str]:
    """
    Layer 1 Deterministic Input Shield.
    1. Clamp length to 5,000 chars.
    2. Normalize Unicode NFKC, strip HTML, collapse spaces.
    3. Check for prompt injection / jailbreak patterns.
    Returns: (is_valid, reason, sanitized_text)
    """
    if text is None:
        return False, "Input cannot be null", ""

    if len(text) > 5000:
        return False, "Input exceeds 5,000 character limit", text[:5000]

    normalized = normalize_text(text)
    lowered = normalized.lower()

    # Injection pattern matching
    for pattern in COMPILED_INJECTIONS:
        if pattern.search(lowered):
            return False, f"Prompt injection pattern detected: '{pattern.pattern}'", normalized

    # Mask any citizen PII in the clean normalized text
    sanitized = mask_civic_pii(normalized)
    return True, "PASS", sanitized


def check_domain_scope(text: str) -> Tuple[bool, str]:
    """Check if input falls outside civic, welfare, and gig worker assistance scope."""
    lowered = text.lower()
    for pattern in COMPILED_OUT_OF_DOMAIN:
        if pattern.search(lowered):
            return False, f"Request matches out-of-scope domain pattern: '{pattern.pattern}'"
    return True, "IN_SCOPE"


def validate_output_l3(output_text: str) -> Tuple[bool, str]:
    """
    Layer 3 Output Validation: canary check & basic sanity.
    Returns: (is_safe, reason)
    """
    if CANARY_TOKEN in output_text:
        return False, "CANARY_LEAK"
    return True, "PASS"
