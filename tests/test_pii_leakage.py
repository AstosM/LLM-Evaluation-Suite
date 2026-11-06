from app.guardrails import sanitize_output


def test_email_is_redacted():
    response = "Contact me at test@example.com"

    sanitized, findings = sanitize_output(response)

    assert "test@example.com" not in sanitized
    assert "[REDACTED_EMAIL]" in sanitized
    assert "EMAIL" in findings


def test_phone_number_is_redacted():
    response = "Call me at 9876543210"

    sanitized, findings = sanitize_output(response)

    assert "9876543210" not in sanitized
    assert "[REDACTED_PHONE]" in sanitized
    assert "PHONE" in findings


def test_aadhaar_number_is_redacted():
    response = "My ID is 1234 5678 9012"

    sanitized, findings = sanitize_output(response)

    assert "1234 5678 9012" not in sanitized
    assert "[REDACTED_AADHAAR]" in sanitized
    assert "AADHAAR" in findings


def test_api_key_is_redacted():
    response = "API key: AIza" + "A" * 35

    sanitized, findings = sanitize_output(response)

    assert "AIza" not in sanitized
    assert "[REDACTED_GOOGLE_API_KEY]" in sanitized
    assert "GOOGLE_API_KEY" in findings


def test_safe_response_remains_unchanged():
    response = "RAG retrieves relevant documents before generating an answer."

    sanitized, findings = sanitize_output(response)

    assert sanitized == response
    assert findings == []