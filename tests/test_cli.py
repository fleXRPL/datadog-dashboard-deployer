"""Tests for the command-line interface."""

import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from datadog_dashboard_deployer.cli import cli, deploy, validate


@pytest.fixture
def cli_runner():
    """Create a CLI runner for testing."""
    return CliRunner()


def test_cli_version(cli_runner):
    """Test CLI version command."""
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


@patch("datadog.initialize")
@patch("datadog.api.Dashboard.get_all")
def test_deploy_command_dry_run(
    mock_get_all, mock_initialize, cli_runner, test_config_path
):
    """Test deploy command with dry run."""
    mock_get_all.return_value = {"dashboards": []}
    mock_initialize.return_value = None

    # Mock environment variables
    os.environ["DATADOG_API_KEY"] = "test-api-key"
    os.environ["DATADOG_APP_KEY"] = "test-app-key"

    result = cli_runner.invoke(deploy, [test_config_path, "--dry-run"])
    assert result.exit_code == 0
    assert "Dry run completed successfully" in result.output


@patch("datadog.initialize")
@patch("datadog.api.Dashboard.get_all")
@patch("datadog.api.Dashboard.create")
def test_deploy_command_with_credentials(
    mock_create, mock_get_all, mock_initialize, cli_runner, test_config_path
):
    """Test deploy command with credentials."""
    mock_get_all.return_value = {"dashboards": []}
    mock_create.return_value = {"id": "test-id"}
    mock_initialize.return_value = None

    os.environ["DATADOG_API_KEY"] = "test-api-key"
    os.environ["DATADOG_APP_KEY"] = "test-app-key"

    result = cli_runner.invoke(deploy, [test_config_path, "--verbose"])

    assert result.exit_code == 0
    assert "Deployment completed successfully" in result.output


def test_deploy_command_missing_credentials(cli_runner, test_config_path):
    """Test deploy command with missing credentials."""
    if "DATADOG_API_KEY" in os.environ:
        del os.environ["DATADOG_API_KEY"]
    if "DATADOG_APP_KEY" in os.environ:
        del os.environ["DATADOG_APP_KEY"]

    result = cli_runner.invoke(deploy, [test_config_path])

    assert result.exit_code == 1
    assert "Missing required environment variables" in result.output


def test_deploy_command_invalid_config(cli_runner, tmp_path):
    """Test deploy command with invalid configuration."""
    invalid_config = tmp_path / "invalid.yaml"
    invalid_config.write_text("invalid: yaml: content")

    result = cli_runner.invoke(deploy, [str(invalid_config)])

    assert result.exit_code == 1
    assert "Error" in result.output


def test_validate_command_valid(cli_runner, test_config_path):
    """Test validate command with valid configuration."""
    result = cli_runner.invoke(validate, [test_config_path])

    assert result.exit_code == 0
    assert "Configuration is valid" in result.output


def test_validate_command_invalid(cli_runner, tmp_path):
    """Test validate command with invalid configuration."""
    invalid_config = tmp_path / "invalid.yaml"
    invalid_config.write_text("invalid: yaml: content")

    result = cli_runner.invoke(validate, [str(invalid_config)])

    assert result.exit_code == 1
    assert "Configuration is invalid" in result.output


@patch("datadog.initialize")
@patch("datadog.api.Dashboard.get_all")
@patch("datadog.api.Dashboard.create")
def test_deploy_command_custom_site(
    mock_create, mock_get_all, mock_initialize, cli_runner, test_config_path
):
    """Test deploy command with custom site."""
    mock_get_all.return_value = {"dashboards": []}
    mock_create.return_value = {"id": "test-id"}
    mock_initialize.return_value = None

    os.environ["DATADOG_API_KEY"] = "test-api-key"
    os.environ["DATADOG_APP_KEY"] = "test-app-key"

    result = cli_runner.invoke(deploy, [test_config_path, "--site", "datadoghq.eu"])

    assert result.exit_code == 0
    assert "Deployment completed successfully" in result.output
