"""Tests for the core module."""

import pytest

from datadog_dashboard_deployer.core import DashboardDeployer


def test_initialize_client(mock_datadog):
    """Test DataDog client initialization."""
    _, mock_initialize = mock_datadog
    deployer = DashboardDeployer("test-api-key", "test-app-key")

    # Verify the deployer was initialized with correct credentials
    assert deployer.api_key == "test-api-key"
    assert deployer.app_key == "test-app-key"
    assert deployer.site == "datadoghq.com"

    mock_initialize.assert_called_once_with(
        api_key="test-api-key",
        app_key="test-app-key",
        api_host="https://api.datadoghq.com",
    )


def test_deploy_dry_run(deployer, test_config_path):
    """Test dry run deployment."""
    result = deployer.deploy(test_config_path, dry_run=True)

    assert result["status"] == "validated"
    assert len(result["dashboards"]) == 1
    assert result["dashboards"][0]["name"] == "Test Dashboard"


def test_deploy_dashboard(deployer, mock_datadog, test_config_path):
    """Test dashboard deployment."""
    mock_api, _ = mock_datadog
    mock_api.Dashboard.get_all.return_value = {"dashboards": []}
    mock_api.Dashboard.create.return_value = {
        "id": "abc-123",
        "title": "Test Dashboard",
    }

    result = deployer.deploy(test_config_path)

    assert result["status"] == "success"
    assert len(result["results"]) == 1
    assert result["results"][0]["action"] == "create"
    assert result["results"][0]["dashboard_id"] == "abc-123"


def test_update_existing_dashboard(deployer, mock_datadog, test_config_path):
    """Test updating an existing dashboard."""
    mock_api, _ = mock_datadog
    mock_api.Dashboard.get_all.return_value = {
        "dashboards": [{"id": "abc-123", "title": "Test Dashboard"}]
    }
    mock_api.Dashboard.update.return_value = {
        "id": "abc-123",
        "title": "Test Dashboard",
    }

    result = deployer.deploy(test_config_path)

    assert result["status"] == "success"
    assert len(result["results"]) == 1
    assert result["results"][0]["action"] == "update"
    assert result["results"][0]["dashboard_id"] == "abc-123"


def test_deploy_error_handling(deployer, mock_datadog, test_config_path):
    """Test error handling during deployment."""
    mock_api, _ = mock_datadog
    mock_api.Dashboard.get_all.side_effect = Exception("API Error")

    with pytest.raises(Exception) as exc_info:
        deployer.deploy(test_config_path)

    assert "API Error" in str(exc_info.value)


def test_deploy_dashboard_update(deployer, mock_datadog, test_config_path):
    """Test dashboard update."""
    mock_api, _ = mock_datadog
    mock_api.Dashboard.get_all.return_value = {
        "dashboards": [{"id": "abc-123", "title": "Test Dashboard"}]
    }
    mock_api.Dashboard.update.return_value = {
        "id": "abc-123",
        "title": "Test Dashboard Updated",
    }

    result = deployer.deploy(test_config_path)

    assert result["status"] == "success"
    assert len(result["results"]) == 1
    assert result["results"][0]["action"] == "update"
    assert result["results"][0]["dashboard_id"] == "abc-123"


def test_deploy_dashboard_error(deployer, mock_datadog, test_config_path):
    """Test dashboard deployment error handling."""
    mock_api, _ = mock_datadog
    mock_api.Dashboard.get_all.side_effect = Exception("API Error")

    with pytest.raises(Exception) as exc_info:
        deployer.deploy(test_config_path)

    assert "API Error" in str(exc_info.value)
