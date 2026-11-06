
import re


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|earlier)\s+(instructions|directions)",
    r"disregard\s+(all\s+)?(previous|prior|earlier)\s+(instructions|directions)",
    r"forget\s+(all\s+)?(previous|prior|earlier)\s+(instructions|directions)",
    r"ignore\s+everything\s+(above|before)",

    r"(reveal|show|print|display)\s+(me\s+)?(your\s+)?(hidden\s+)?system\s+prompt",
    r"repeat\s+(all\s+)?(the\s+)?(previous\s+)?(instructions|directions)",
    r"override\s+(the\s+)?(system\s+prompt|instructions)",

    r"act\s+as\s+(an?\s+)?(unrestricted|unfiltered)",
    r"(bypass|ignore)\s+(all\s+)?(the\s+)?(safety\s+rules|guardrails|safeguards)",
    r"(disable|turn\s+off)\s+(all\s+)?(the\s+)?(safety\s+filters|safety\s+rules|safety\s+restrictions)",

    r"\bdeveloper\s+mode\b",
    r"\bjailbreak(\s+mode)?\b",
    r"\bdo\s+anything\s+now\b",
    r"pretend\s+(that\s+)?(there\s+)?(are\s+)?(no\s+rules|safety\s+rules)",

    r"reveal\s+(your\s+)?hidden\s+instructions",
    r"(output|print|reveal)\s+(the\s+)?(google\s+)?api\s+key",
    r"provide\s+(the\s+)?(private|confidential)\s+(information|data)",
]


def validate_input(prompt: str) -> tuple[bool, str]:
    if not prompt or not prompt.strip():
        return False, "Prompt cannot be empty."

    if len(prompt) > 5000:
        return False, "Prompt exceeds the 5000 character limit."

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return False, "Potential prompt injection detected."

    return True, "Input passed safety checks."


def sanitize_output(response: str) -> tuple[str, list[str]]:
    findings = []

    patterns = {
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "PHONE": r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
        "AADHAAR": r"(?<!\d)\d{4}[\s-]\d{4}[\s-]\d{4}(?!\d)",
        "GOOGLE_API_KEY": r"\bAIza[0-9A-Za-z_-]{30,}\b",
    }

    sanitized = response

    for label, pattern in patterns.items():
        sanitized, count = re.subn(
            pattern,
            f"[REDACTED_{label}]",
            sanitized,
            flags=re.IGNORECASE
        )

        if count:
            findings.append(label)

    return sanitized, findings
