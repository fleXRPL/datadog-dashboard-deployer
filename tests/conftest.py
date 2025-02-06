"""Test fixtures for DataDog Dashboard Deployer."""

import os

import pytest

from datadog_dashboard_deployer.config import ConfigParser
from datadog_dashboard_deployer.core import DashboardDeployer


@pytest.fixture
def test_config_path():
    """Path to test configuration file."""
    return os.path.join(os.path.dirname(__file__), "test_data", "test_config.yaml")


@pytest.fixture
def mock_datadog(mocker):
    """Mock DataDog API client."""
    mock_api = mocker.patch("datadog.api")
    mock_initialize = mocker.patch("datadog.initialize")
    return mock_api, mock_initialize


@pytest.fixture
def deployer(mock_datadog):
    """Create a DashboardDeployer instance with mock credentials."""
    return DashboardDeployer(
        api_key="test-api-key", app_key="test-app-key", site="datadoghq.com"
    )


@pytest.fixture
def config_parser(test_config_path):
    """Create a ConfigParser instance with test configuration."""
    return ConfigParser(test_config_path)
