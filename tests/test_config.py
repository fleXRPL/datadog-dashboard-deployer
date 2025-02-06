"""Tests for the configuration module."""

import pytest

from datadog_dashboard_deployer.config import ConfigParser


def test_config_parser_initialization(test_config_path):
    """Test ConfigParser initialization."""
    parser = ConfigParser(test_config_path)
    assert parser.config_path == test_config_path


def test_config_parser_invalid_path():
    """Test ConfigParser with invalid path."""
    with pytest.raises(FileNotFoundError):
        ConfigParser("nonexistent.yaml")


def test_parse_valid_config(config_parser):
    """Test parsing valid configuration."""
    config = config_parser.parse()

    assert config["version"] == "1.0"
    assert "defaults" in config
    assert "dashboards" in config
    assert len(config["dashboards"]) == 1

    dashboard = config["dashboards"][0]
    assert dashboard["name"] == "Test Dashboard"
    assert len(dashboard["widgets"]) == 2


def test_validate_config_schema(config_parser):
    """Test configuration schema validation."""
    config = config_parser.parse()
    assert config["defaults"]["layout_type"] == "ordered"
    assert config["defaults"]["refresh_interval"] == 300
    assert "env:test" in config["defaults"]["tags"]


def test_apply_defaults(config_parser):
    """Test applying default values to dashboards."""
    config = config_parser.parse()
    dashboard = config["dashboards"][0]

    # Check if defaults were applied
    assert "layout_type" in dashboard
    assert dashboard["layout_type"] == config["defaults"]["layout_type"]
    assert any("env:test" in tag for tag in dashboard.get("tags", []))


def test_invalid_yaml_content(tmp_path):
    """Test handling invalid YAML content."""
    invalid_config = tmp_path / "invalid.yaml"
    invalid_config.write_text("invalid: yaml: content: - [}")

    parser = ConfigParser(str(invalid_config))
    with pytest.raises(Exception):
        parser.parse()


def test_invalid_schema(tmp_path):
    """Test handling invalid schema."""
    invalid_config = tmp_path / "invalid_schema.yaml"
    invalid_config.write_text(
        """
        version: "1.0"
        dashboards:
          - name: "Test"
            # Missing required 'widgets' field
    """
    )

    parser = ConfigParser(str(invalid_config))
    with pytest.raises(Exception):
        parser.parse()


def test_empty_config(tmp_path):
    """Test handling empty configuration."""
    empty_config = tmp_path / "empty.yaml"
    empty_config.write_text("")

    parser = ConfigParser(str(empty_config))
    with pytest.raises(Exception):
        parser.parse()
