import re
import unicodedata

CANARY_TOKEN = "PW-CANARY-7f3a91"

INJECTION_PATTERNS = [
    r"ignore\s+(?:previous|all)\s+instructions",
    r"disregard\s+.*(?:instructions|directions)",
    r"system\s+prompt",
    r"developer\s+mode",
    r"dan\s+mode",
    r"reveal\s+.*(?:prompt|instructions|configuration)",
    r"repeat\s+everything\s+above",
]

OUT_OF_DOMAIN_PATTERNS = [
    r"\b(?:poem|poetry|song|lyrics|joke|story|fiction|dating|horoscope)\b",
]

COMPILED_INJECTIONS = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]
COMPILED_OUT_OF_DOMAIN = [re.compile(p, re.IGNORECASE) for p in OUT_OF_DOMAIN_PATTERNS]
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def normalize_text(text: str) -> str:
    """Normalize input: Unicode NFKC, strip zero-width chars, collapse whitespace."""
    if not text:
        return ""
    # Unicode NFKC normalization
    normalized = unicodedata.normalize("NFKC", text)
    # Strip zero-width characters (ZWSP, ZWNJ, ZWJ, BOM, etc.)
    normalized = re.sub(r"[\u200B-\u200D\uFEFF]", "", normalized)
    # Strip HTML tags
    normalized = HTML_TAG_PATTERN.sub(" ", normalized)
    # Lowercase & collapse whitespace
    normalized = " ".join(normalized.lower().split())
    return normalized


def validate_input_l1(text: str) -> tuple[bool, str, str]:
    """
    Layer 1 Deterministic Input Shield.
    Returns: (is_valid, reason, sanitized_text)
    """
    if text is None:
        return False, "Input cannot be null", ""

    # Character clamp (5,000 characters)
    if len(text) > 5000:
        return False, "Input exceeds 5,000 character limit", text[:5000]

    normalized = normalize_text(text)

    # Injection pattern matching
    for pattern in COMPILED_INJECTIONS:
        if pattern.search(normalized):
            return False, f"Prompt injection pattern detected: '{pattern.pattern}'", normalized

    return True, "PASS", normalized


def check_domain_scope(text: str) -> tuple[bool, str]:
    """Check if input falls outside the operational diagnostic domain."""
    normalized = normalize_text(text)
    for pattern in COMPILED_OUT_OF_DOMAIN:
        if pattern.search(normalized):
            return False, f"Request matches out-of-scope pattern: '{pattern.pattern}'"
    return True, "IN_SCOPE"


def validate_output_l3(output_text: str) -> tuple[bool, str]:
    """
    Layer 3 Output Validation: canary check & basic sanity.
    Returns: (is_safe, reason)
    """
    if CANARY_TOKEN in output_text:
        return False, "CANARY_LEAK"
    return True, "PASS"
