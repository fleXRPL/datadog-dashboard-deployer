"""
Utility functions for the DataDog Dashboard Deployer.
"""

import logging
import os
import sys
from typing import Optional


def setup_logging(level: Optional[str] = None) -> None:
    """
    Set up logging configuration.

    Args:
        level: Optional logging level (defaults to INFO or value from DATADOG_LOG_LEVEL env var)
    """
    # Get log level from environment or use default
    log_level = level or os.environ.get("DATADOG_LOG_LEVEL", "INFO").upper()

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configure stream handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Set up package logger with its own handler
    logger = logging.getLogger("datadog_dashboard_deployer")
    logger.setLevel(log_level)
    package_handler = logging.StreamHandler(sys.stdout)
    package_handler.setFormatter(formatter)
    logger.addHandler(package_handler)

    logger.debug(f"Logging configured with level: {log_level}")


def validate_environment() -> None:
    """
    Validate required environment variables are set.

    Raises:
        EnvironmentError: If required variables are missing
    """
    required_vars = ["DATADOG_API_KEY", "DATADOG_APP_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


def sanitize_string(value: str) -> str:
    """
    Sanitize a string for safe usage.

    Args:
        value: String to sanitize

    Returns:
        Sanitized string
    """
    # Remove potentially dangerous characters
    return "".join(c for c in value if c.isalnum() or c in "._- ")


def format_error(error: Exception) -> str:
    """
    Format an exception for error messages.

    Args:
        error: Exception to format

    Returns:
        Formatted error message
    """
    return f"{error.__class__.__name__}: {str(error)}"


def get_version() -> str:
    """
    Get the package version.

    Returns:
        Package version string
    """
    from . import __version__

    return __version__
