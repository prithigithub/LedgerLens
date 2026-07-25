from backend.services.pii import redact_pii


def test_email_redaction():
    result = redact_pii("Contact test@example.com")
    assert "test@example.com" not in result
    assert "EMAIL_REDACTED" in result


def test_phone_redaction():
    result = redact_pii("Call +91 98765 43210")
    assert "98765 43210" not in result
    assert "PHONE_REDACTED" in result


def test_ssn_redaction():
    result = redact_pii("SSN 123-45-6789")
    assert "123-45-6789" not in result
    assert "SSN_REDACTED" in result
