"""Tests for the utilities module."""

import logging
import os

import pytest

from datadog_dashboard_deployer.utils import (
    format_error,
    get_version,
    sanitize_string,
    setup_logging,
    validate_environment,
)


def test_setup_logging():
    """Test logging setup."""
    setup_logging("DEBUG")
    logger = logging.getLogger("datadog_dashboard_deployer")

    assert logger.level == logging.DEBUG
    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_setup_logging_default_level():
    """Test logging setup with default level."""
    setup_logging()
    logger = logging.getLogger("datadog_dashboard_deployer")

    assert logger.level == logging.INFO


def test_validate_environment_valid():
    """Test environment validation with valid variables."""
    os.environ["DATADOG_API_KEY"] = "test-api-key"
    os.environ["DATADOG_APP_KEY"] = "test-app-key"

    # Should not raise an exception
    validate_environment()


def test_validate_environment_missing(monkeypatch):
    """Test environment validation with missing variables."""
    # Safely remove environment variables using monkeypatch
    monkeypatch.delenv("DATADOG_API_KEY", raising=False)
    monkeypatch.delenv("DATADOG_APP_KEY", raising=False)

    with pytest.raises(EnvironmentError) as exc_info:
        validate_environment()

    assert "Missing required environment variables" in str(exc_info.value)


def test_sanitize_string():
    """Test string sanitization."""
    test_cases = [
        ("Hello World", "Hello World"),
        ("Test-123_.", "Test-123_."),
        ("Bad!@#$Chars", "BadChars"),
        ("", ""),
        ("   spaces   ", "   spaces   "),
    ]

    for input_str, expected in test_cases:
        assert sanitize_string(input_str) == expected


def test_format_error():
    """Test error formatting."""
    error = ValueError("Test error message")
    formatted = format_error(error)

    assert "ValueError" in formatted
    assert "Test error message" in formatted


def test_get_version():
    """Test version retrieval."""
    version = get_version()

    assert isinstance(version, str)
    assert len(version.split(".")) == 3
